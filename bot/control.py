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
    if not config.control_chat_id:
        return
    if msg.chat.id != config.control_chat_id or Undefined.default(msg.message_thread_id) != config.control_chat_thread_id:
        return
    msg_id = None
    msg_chat_id = None
    for player in User.get_all_players(db_sess):
        ok, msgid = tgapi.copyMessage(player.id_tg, None, msg.chat.id, msg.message_id)
        if ok and msg_id is None:
            msg_id = msgid
            msg_chat_id = player.id_tg
    if msg_id and msg_chat_id and config.broadcast_chat_id:
        tgapi.forwardMessage(config.broadcast_chat_id, config.broadcast_chat_thread_id,
                             msg_chat_id, msg_id.message_id, disable_notification=True)
