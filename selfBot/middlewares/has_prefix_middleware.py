import json
from vkbottle import BaseMiddleware
from time import sleep


class HasPrefixMiddleware(BaseMiddleware):
    """
    Миддлварь, который отсеивает сообщения,
    которые не начинаются с префикса
    """

    async def pre(self):
        with open("config.json", "r", encoding="utf-8") as file:
            content = json.load(file)
        if content.get("ai_mode", True):
            return
        else:
            if not self.event.text.startswith(content["prefix"]):
                self.stop("Сообщение не начинается с префикса")
