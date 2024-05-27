"""
Roleplay commands (!me, !бросить кактус, etc.)
"""
from vkbottle.user import Blueprint, Message

from utils.edit_msg import edit_msg
from utils.emojis import ERROR
from filters import ForEveryoneRule

bp = Blueprint("Interactive commands")


class Interactive:
    def __init__(
        self, api, message: Message, split_to: int, name_case: str = "acc"
    ):
        self.api = api
        self.message = message
        self.split_to = split_to
        self.name_case = name_case

    async def get_my_name(self) -> str:
        """
        Returns first name and last name
        """
        response = await self.api.users.get(
            user_ids=self.message.from_id, fields="first_name,last_name"
        )
        return (
            f"{response[0].first_name} {response[0].last_name}"
        )

    async def get_target_name(self) -> str:
        """
        672876228 -> [id672876228|Вячеслав Бебровский]
        """
        if len(self.message.text.split()) > self.split_to:
            mention = self.message.text.split()[self.split_to]
            if mention.startswith("["):
                who = mention.split("|")[0][1:].replace(
                    "id", ""
                )
                response = await self.api.users.get(
                    user_ids=who,
                    fields="first_name,last_name",
                    name_case=self.name_case,
                )
                return (
                    "[id"
                    f"{who}|{response[0].first_name} {response[0].last_name}"
                    "]"
                )

            else:
                await edit_msg(
                    bp.api,
                    self.message,
                    text=(
                        f"{ERROR} | Вы написали не упоминание, а какую ту "
                        "чушь!"
                    )
                )

        elif self.message.reply_message is not None:
            who = self.message.reply_message.from_id
            response = await self.api.users.get(
                user_ids=who,
                fields="first_name,last_name",
                name_case=self.name_case,
            )
            return (
                f"[id{who}|{response[0].first_name} {response[0].last_name}]"
            )

        else:
            await edit_msg(
                bp.api,
                self.message,
                text=f"{ERROR} | Вы не ответили никому!",
            )


@bp.on.message(
    ForEveryoneRule("roleplay"), text="<prefix>me <action>"
)
async def me_handler(message: Message, action):
    """
    > !me съел суши
    > Вячеслав Бебровский съел суши 💬
    """
    who = await bp.api.users.get(user_ids=message.from_id)
    name = who[0].first_name
    last_name = who[0].last_name
    await edit_msg(
        bp.api, message, text=f"{name} {last_name} {action} &#128172;"
    )


@bp.on.message(
    ForEveryoneRule("roleplay"),
    text=["<prefix>бонкнуть", "<prefix>бонкнуть <mention>"],
)
async def bonk_handler(message: Message):
    """
    > !бонкнуть @username
    > Вячеслав Бебровский бонкнул Usera 🧹
    """
    interactive = Interactive(bp.api, message, 1)
    await edit_msg(
        bp.api,
        message,
        text=(
            f"{await interactive.get_my_name()} бонкнул "
            f"{await interactive.get_target_name()} &#129529;"
        )
    )


@bp.on.message(
    ForEveryoneRule("roleplay"),
    text=["<prefix>бросить кактус", "<prefix>бросить кактус <mention>"],
)
async def cactus_handler(message: Message):
    """
    > !бросить кактус @username
    > Вячеслав Бебровский бросил кактус в Usera 🌵
    """
    interactive = Interactive(bp.api, message, 2)
    await edit_msg(
        bp.api,
        message,
        text=(
            f"{await interactive.get_my_name()} бросил кактус в "
            f"{await interactive.get_target_name()} &#127797;"
        )
    )


@bp.on.message(
    ForEveryoneRule("roleplay"),
    text=["<prefix>поцеловать", "<prefix>поцеловать <mention>",
          "<prefix>kiss <mention>", "<prefix>kiss"],
)
async def cactus_handler(message: Message):
    """
    > !поцеловать @username
    > Вячеслав Бебровский поцеловал Usera 🌵
    """
    interactive = Interactive(bp.api, message, 2)
    await edit_msg(
        bp.api,
        message,
        text=(
            f"{await interactive.get_my_name()} поцеловал "
            f"{await interactive.get_target_name()} &#128139;"
        )
    )
    
    
@bp.on.message(
    ForEveryoneRule("roleplay"),
    text=["<prefix>обнять", "<prefix>обнять <mention>", "<prefix>hug <mention>", "<prefix>hug"],
)
async def hug_handler(message: Message):
    """
    > !обнять @username
    > Вячеслав Бебровский обнял Usera 🤗
    """
    interactive = Interactive(bp.api, message, 2)
    await edit_msg(
        bp.api,
        message,
        text=(
            f"{await interactive.get_my_name()} обнял "
            f"{await interactive.get_target_name()} &#129303;"
        )
    )


@bp.on.message(
    ForEveryoneRule("roleplay"),
    text=["<prefix>похвалить", "<prefix>похвалить <mention>",
          "<prefix>praise <mention>", "<prefix>praise"],
)
async def praise_handler(message: Message):
    """
    > !похвалить @username
    > Вячеслав Бебровский похвалил Usera 🎉
    """
    interactive = Interactive(bp.api, message, 2)
    await edit_msg(
        bp.api,
        message,
        text=(
            f"{await interactive.get_my_name()} похвалил "
            f"{await interactive.get_target_name()} &#127881;"
        )
    )
