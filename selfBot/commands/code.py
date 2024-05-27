"""
Эта команда позволяет интерпретировать Python-код
"""
from vkbottle.bot import Blueprint, Message
import subprocess

from utils.edit_msg import edit_msg
from filters import ForEveryoneRule


bp = Blueprint("Code executer command")


@bp.on.message(ForEveryoneRule("code"), text="<prefix>код<!>\n<!>")
async def code_handler(message: Message):
    """
    > !код
    > a = 5
    > b = 10
    > if b > a:
    >     c = b + a

    > a: int = 5
    > b: int = 10
    > c: int = 15
    """
    txt = '\n'.join(message.text.split("\n")[1:])
    code = txt.replace("~", " ")
    
    with open("output/code.py", "w") as f:
        f.write(code)
    try:
        output = subprocess.check_output(['python', 'output/code.py'])
        result = f"Вывод:\n{output.decode('utf-8')}"
    except subprocess.CalledProcessError as e:
        result = f"Ошибка:\n{e.returncode}"
    await edit_msg(bp.api, message, result)
