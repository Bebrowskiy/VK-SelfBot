from vkbottle.user import Blueprint, Message
from g4f.client import Client

from utils.edit_msg import edit_msg
from utils.emojis import ERROR
from filters import ForEveryoneRule


bp = Blueprint('Artificial intelligence')


class AI:
    def __init__(self, message: Message, client: Client):
        self.message = message
        self.client = client

    async def get_response(self, question: str):
        client = self.client()
        response = client.chat.completions.create(
            model="blackbox",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content
        return answer
    
    
@bp.on.message(
    ForEveryoneRule("ai"), text="<prefix>ai <action>"
)
async def ai(message: Message, action):
    """
    > !me съел суши
    > Тимур Богданов съел суши 💬
    """
    ai_request = AI(message, Client)
    response = await ai_request.get_response(action)
    await edit_msg(
        bp.api, message, text=f"Ответ: {response[13:]} &#128172;"
    )
