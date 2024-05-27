"""

Image Generation commands(demotivator, quote, etc.)

"""

from vkbottle.bot import Blueprint, Message
from vkbottle.tools import PhotoMessageUploader
from simpledemotivators import Demotivator, Quote
from typing import Optional

from utils.edit_msg import edit_msg
from filters import ForEveryoneRule
from utils.emojis import ERROR
from utils.request_url import request

bp = Blueprint('Image generator')


class ImageGenerator:
    def __init__(
        self, api, message: Message):
        self.api = api
        self.message = message
        

@bp.on.message(ForEveryoneRule("image"), text=["<prefix>цитата"])
async def quote(message: Message):
    """
    > !цитата (ответ на сообщение)
    """

    if message.reply_message is None:
        await edit_msg(
            bp.api,
            message,
            f"{ERROR} | Вы не ответили на сообщение!",
        )
        return
    elif message.reply_message.text == "":
        await edit_msg(
            bp.api,
            message,
            f"{ERROR} | Сообщение пустое! (картинка, стикер?)",
        )
        return

    reply_text = ""+message.reply_message.text+""
    reply_user_id = message.reply_message.from_id
    reply_response = await bp.api.users.get(
        user_ids=reply_user_id, fields="first_name,last_name"
    )

    author_name = (
        f"{reply_response[0].first_name} {reply_response[0].last_name}"
    )

    author = await bp.api.users.get(reply_user_id, fields="photo_400_orig")
    author_photo_url = author[0].photo_400_orig
    author_photo = await request(author_photo_url)
    with open("output/quote_author.png", "wb") as file:
        file.write(author_photo)

    quote = Quote(quote_text=reply_text, author_name=author_name)
    quote.create(file="output/quote_author.png",
                 quote_text_font="sources/fonts/Montserrat-MediumItalic.ttf",
                 headline_text_font="sources/fonts/Montserrat-MediumItalic.ttf",
                 author_name_font="sources/fonts/Montserrat-MediumItalic.ttf",
                 result_filename="output/quote_result.png")

    # Saving and uploading image
    attachment = await PhotoMessageUploader(bp.api).upload(
        "output/quote_result.png", peer_id=message.peer_id
    )
    await edit_msg(
        bp.api,
        message,
        attachment=attachment,
    )


@bp.on.message(
    ForEveryoneRule("image"),
    text=[
        "<prefix>дем <first_text>|<second_text>",
        "<prefix>дем <first_text>",
        "<prefix>дем |<second_text>",
        "<prefix>демотиватор <first_text>|<second_text>",
        "<prefix>демотиватор <first_text>",
        "<prefix>демотиватор |<second_text>",
        "<prefix>demotivator <first_text>|<second_text>",
        "<prefix>demotivator <first_text>",
        "<prefix>demotivator |<second_text>",
        "<prefix>dem <first_text>|<second_text>",
        "<prefix>dem <first_text>",
        "<prefix>dem |<second_text>",
    ],
)
async def demotivator(
    message: Message,
    first_text: Optional[str] = "",
    second_text: Optional[str] = "",
):
    """
    > !дем [текст1]|[текст2]
    > !дем [текст1]
    > !дем |[текст2]
    """

    if len(message.attachments) > 0:
        url = message.attachments[0].photo.sizes[-1].url
        photo_bytes = await request(url)

        with open("output/dem_output.png", "wb") as file:
            file.write(photo_bytes)
    else:
        await edit_msg(
            bp.api, message, f"{ERROR} | Вы не прикрепили фото к сообщению!"
        )
        return

    dem = Demotivator(top_text=first_text, bottom_text=second_text)
    dem.create(file="output/dem_output.png",
               font_name="sources/fonts/Montserrat-MediumItalic.ttf",
               result_filename="output/dem_result.png"
            )

    # Saving and uploading image
    attachment = await PhotoMessageUploader(bp.api).upload(
        "output/dem_result.png", peer_id=message.peer_id
    )
    await edit_msg(bp.api, message, attachment=attachment)
