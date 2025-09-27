import bafser_tgapi as tgapi

from data.user import User


class Bot(tgapi.BotWithDB[User]):
    _userCls = User


@Bot.on_message
def on_message(bot: Bot):
    assert bot.message
    bot.sendMessage(bot.message.text, entities=bot.message.entities)
