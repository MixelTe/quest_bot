import bafser_tgapi as tgapi
from bafser import Undefined, db_session
from sqlalchemy.orm import Session

from bot.bot import Bot
from data.config import Config
from data.user import User
from utils import reply_markup

ME = tgapi.MessageEntity


@Bot.add_command()
@Bot.cmd_connect_db
def clear_state(bot: Bot, args: tgapi.BotCmdArgs, **_: str):
    assert bot.user
    bot.user.set_state("")


@Bot.add_command()
@Bot.cmd_connect_db
def set_state(bot: Bot, args: tgapi.BotCmdArgs, **_: str):
    assert bot.db_sess
    assert bot.user
    if not bot.user.is_admin():
        return
    if len(args) == 0:
        bot.sendMessage("Select state:", reply_markup=reply_markup(
            [("Начало (started)", "set_state started"), ("Утки (task1)", "set_state task1")],
            [("Озон: Винницкая, 15 (task2)", "set_state task2"), ("Пожарник (task3)", "set_state task3")],
            [("Сытый лис (task4)", "set_state task4"), ("Шар на площади (task5)", "set_state task5")],
            [("Камни у памятника (task6)", "set_state task6"), ("Вкусно не точка (task7)", "set_state task7")],
            [("Озон: Раменки, д.6 к.2 (task8)", "set_state task8"), ("Длинный дом (task9)", "set_state task9")],
            [("Финальный код (task10)", "set_state task10"), ("Конец (quest_end)", "set_state quest_end")],
        ))
        return
    state = args[0]
    if state not in ("started", "task1", "task2", "task3", "task4", "task5",
                     "task6", "task7", "task8", "task9", "task10", "quest_end"):
        return "wrong state name"
    changed = ""
    for player in User.get_all_players(bot.db_sess):
        changed += player.get_name() + f" ({player.get_tagname()})\n"
        player.set_state(state)
    return f"state \"{state}\" are set for:\n{changed}"


@Bot.add_command()
@Bot.cmd_connect_db
@Bot.cmd_for_admin
def set_control(bot: Bot, args: tgapi.BotCmdArgs, **_: str):
    assert bot.db_sess
    assert bot.user
    assert bot.message
    if not bot.user.is_admin():
        return
    config = Config.get(bot.db_sess)
    config.set_control_chat(bot.user, bot.message.chat.id, Undefined.default(bot.message.message_thread_id))


@Bot.add_command()
@Bot.cmd_connect_db
@Bot.cmd_for_admin
def set_broadcast(bot: Bot, args: tgapi.BotCmdArgs, **_: str):
    assert bot.db_sess
    assert bot.user
    assert bot.message
    if not bot.user.is_admin():
        return
    config = Config.get(bot.db_sess)
    config.set_broadcast_chat(bot.user, bot.message.chat.id, Undefined.default(bot.message.message_thread_id))


def forward(r: tuple[bool, tgapi.Message]):
    ok, msg = r
    if isinstance(msg, tgapi.Message):
        with db_session.create_session() as db_sess:
            config = Config.get(db_sess)
            if not config.broadcast_chat_id:
                return
            tgapi.forwardMessage(config.broadcast_chat_id, config.broadcast_chat_thread_id,
                                 msg.chat.id, msg.message_id, disable_notification=True)


def send_as_bot(db_sess: Session, msg: tgapi.Message):
    config = Config.get(db_sess)
    if not config.broadcast_chat_id:
        return
    if msg.chat.id != config.broadcast_chat_id or Undefined.default(msg.message_thread_id) != config.broadcast_chat_thread_id:
        return
    msg_id = None
    msg_chat_id = None
    for player in User.get_all_players(db_sess):
        ok, msgid = tgapi.copyMessage(player.id_tg, None, msg.chat.id, msg.message_id)
        if ok and msg_id is None:
            msg_id = msgid
            msg_chat_id = player.id_tg
    tgapi.deleteMessage(msg.chat.id, msg.message_id)
    if msg_id and msg_chat_id:
        tgapi.forwardMessage(config.broadcast_chat_id, config.broadcast_chat_thread_id,
                             msg_chat_id, msg_id.message_id, disable_notification=True)


def on_state_update(user: User):
    db_sess = Session.object_session(user)
    assert db_sess
    config = Config.get(db_sess)
    if not config.control_chat_id:
        return
    texts = []
    for player in User.get_all_players(db_sess):
        text = player.get_name() + f" ({player.get_tagname()})\n"
        state = player.state
        match state:
            case "started": state = "Начало"
            case "task1": state = "Утки"
            case "task2": state = "Озон: Винницкая, 15"
            case "task3": state = "Пожарник"
            case "task4": state = "Сытый лис"
            case "task5": state = "Шар на площади"
            case "task6": state = "Камни у памятника"
            case "task7": state = "Вкусно не точка"
            case "task8": state = "Озон: Раменки, д.6 к.2"
            case "task9": state = "Длинный дом"
            case "task10": state = "Финальный код"
            case "quest_end": state = "Конец"
        text += f"Текущий этап: {state}"
        texts.append(text)

    text = "Положение дел:\n\n"
    text += "\n----------\n".join(texts)
    tgapi.sendMessage(config.control_chat_id, text, config.control_chat_thread_id)
