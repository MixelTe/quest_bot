import bafser_tgapi as tgapi

from data.user import User


class Bot(tgapi.BotWithDB[User]):
    _userCls = User


@Bot.on_message
def on_message(bot: Bot):
    from bot.control import forward, send_as_bot
    from bot.story import answer_story
    assert bot.message
    if bot.message.chat.type != "private":
        send_as_bot(bot.db_sess, bot.message)
        return
    forward((True, bot.message))
    if not bot.user.state:
        forward(bot.sendMessage(f"{bot.user.get_name()}?\nНе помню такого...\nВ бан тебя!"))
        bot.user.set_state("banned")
        return
    if bot.user.state == "banned":
        return
    answer_story(bot)
