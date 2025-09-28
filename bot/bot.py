import bafser_tgapi as tgapi

from data.user import User


class Bot(tgapi.BotWithDB[User]):
    _userCls = User


@Bot.on_message
@Bot.connect_db
def on_message(bot: Bot):
    from bot.story import answer_story
    assert bot.message
    assert bot.db_sess
    assert bot.user
    if not bot.user.state:
        bot.sendMessage(f"{bot.user.get_name()}?\nНе помню такого...\nВ бан тебя!")
        bot.user.set_state("banned")
        return
    if bot.user.state == "banned":
        return
    answer_story(bot)
