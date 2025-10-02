import bafser_tgapi as tgapi
from bafser import Undefined

from bot.bot import Bot
from bot.control import forward
from bot.story import answer_story
from utils import reply_markup

ME = tgapi.MessageEntity


@Bot.add_command()
def start(bot: Bot, args: tgapi.BotCmdArgs, **_: str):
    if len(args) < 1 or args[0] != "verySecretStartCode":
        if not bot.user.state:
            bot.user.set_state("banned")
            return f"{bot.user.get_name()}?\nНе помню такого...\nВ бан тебя! 🤪"
        return

    bot.user.set_state("started")
    answer_story(bot)


@Bot.add_command()
def start_quest(bot: Bot, args: tgapi.BotCmdArgs, **_: str):
    if bot.user.state != "started":
        return
    bot.user.set_state("task1")
    answer_story(bot)


@Bot.add_command()
def task_hint(bot: Bot, args: tgapi.BotCmdArgs, **_: str):
    hint = ""
    hintI = ""
    match bot.user.state:
        case "task1":
            hint = "Посреди поля лежит зеркало: стекло голубое, рама зелёная"
        case "task2":
            hint = "слайм"
        case "task3":
            if len(args) > 0 and args[0] == "1":
                sendPhoto(bot, "task3_hint.jpg", "Подсказка 2")
            else:
                p1 = "Подсказка 1:\n"
                p2 = """
В брезентовой куртке и каске,
Забыв про кольчужную бронь,
Решительно и без опаски
Бросается рыцарь в огонь!
""".strip()
                txt = p1 + p2
                forward(bot.sendMessage(txt, entities=[ME.blockquote(ME.len(p1), ME.len(p2))]))
                edit_hint_btns(bot, 2)
        case "task4":
            sendPhoto(bot, "task4_hint.jpg", "Подсказка")
        case "task5":
            sendPhoto(bot, "task5_hint.jpg", "Подсказка")
        case "task6":
            sendPhoto(bot, "task6_hint.jpg", "Подсказка")
        case "task7":
            sendPhoto(bot, "task7_hint.jpg", "Подсказка")
        case "task8":
            if len(args) > 0 and args[0] == "1":
                hintI = " 2"
                hint = "озон"
            else:
                forward(bot.sendMessage("Подсказка 1:\n4 латинских буквы"))
                edit_hint_btns(bot, 2)
        case "task9":
            hint = "ха! а нету подсказки)"
        case "task10":
            hint = "ха! а нету подсказки)"

    if hint:
        forward(bot.sendMessage(f"Подсказка{hintI}:\n" + hint))


def edit_hint_btns(bot: Bot, count: int):
    if bot.callback_query and Undefined.defined(bot.callback_query.message):
        tgapi.editMessageReplyMarkup(bot.callback_query.message.chat.id, bot.callback_query.message.message_id,
                                     reply_markup=reply_markup([
                                         (f"Подсказка {i + 1}", f"task_hint {i}") for i in range(count)
                                     ]))


def sendPhoto(bot: Bot, fname: str, caption: str):
    ok, r = bot.sendPhoto(tgapi.url_for("img.img", fname=fname), caption=caption)
    if not ok:
        ok, r = bot.sendPhoto(tgapi.url_for("img.img", fname=fname, _double_slash=False), caption=caption)
    forward((ok, r))
