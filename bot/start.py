import bafser_tgapi as tgapi

from bot.bot import Bot
from bot.story import answer_story


@Bot.add_command("start")
@Bot.cmd_connect_db
def start(bot: Bot, args: tgapi.BotCmdArgs, **_: str):
    assert bot.db_sess
    assert bot.user
    if len(args) < 1 or args[0] != "theVerySecretStartCode":
        if not bot.user.state:
            bot.user.set_state("banned")
            return f"{bot.user.get_name()}?\nНе помню такого...\nВ бан тебя! 🤪"
        return

    bot.user.set_state("started")
    answer_story(bot)
