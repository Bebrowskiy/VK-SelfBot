from vkbottle.user import Blueprint, Message
from g4f.client import AsyncClient

from utils.edit_msg import edit_msg
from filters import ForEveryoneRule
import json


bp = Blueprint('Artificial intelligence')


class AI:
    def __init__(self, message: Message, client: AsyncClient):
        self.message = message
        self.client = client

    async def stream(self, response: str, model: str, token: str):
        client = self.client()
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": response}],
            stream=True,
            token=token
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                return chunk.choices[0].delta.content or ""

    def load_config():
        with open("config.json", "r", encoding='utf-8') as f:
            return json.load(f)

    def save_config(config):
        with open("config.json", "w", encoding='utf-8') as f:
            json.dump(config, f, indent=4)


@bp.on.message(ForEveryoneRule("ai_mode"), text="<prefix>ai")
async def ai_mode(message: Message):
    config = AI.load_config()
    config["ai_mode"] = not config["ai_mode"]
    AI.save_config(config)

    status = "включен" if config["ai_mode"] else "выключен"
    await edit_msg(bp.api, message, f"Режим ИИ {status} &#128172;")


@bp.on.message(ForEveryoneRule("ai_mode"))
async def handle_message(message: Message):
    config = AI.load_config()
    ignor_user = int(config.get("user_id"))

    if message.from_id == ignor_user:
        return

    if config.get("ai_mode", False):
        ai_request = AI(message, AsyncClient)
        model = config.get("model")
        token = config.get("ai_token")
        response = await ai_request.stream(model=model, token=token, response=message.text)
        await edit_msg(bp.api, message, text=f'{response}')
