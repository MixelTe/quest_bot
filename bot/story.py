from time import sleep
from typing import Callable

import bafser_tgapi as tgapi

from bot.bot import Bot
from data.user import User

type tfn = Callable[[Bot, User], None]
_story_parts: dict[str, tfn] = {}


def answer_story(bot: Bot):
    assert bot.message
    assert bot.db_sess
    assert bot.user
    fn = _story_parts.get(bot.user.state)
    if fn:
        fn(bot, bot.user)
    else:
        bot.sendMessage("ВЕЛИКА ОЩИБКА!")


def story_part(fn: tfn):
    _story_parts[fn.__name__] = fn
    return fn


@story_part
def started(bot: Bot, user: User):
    state, args = user.get_state()
    if args[0] == 1:
        return
    user.set_state(state, [1])
    for msg in [
        "Hi\\!",
        "Повторяю свой *Ультиматум*\\!",
        "Я вас пробил по айпи",
        "Вы меня не позвали на день рождения и теперь *пожалеете* об этом\\!",
        "Подготовил для вас подарочек \\-  *250к тонн тротила* на вас 😂",
        "Хотите спасти свои постройки \\- найдите координаты моего тайника, в котором лежит 145 шалкеров ТНТ, а еще у меня заложник из другого измерения",  # noqa E501
        "Следуйте за вопросами, находите ответы и трепещите от страха 🤪",
    ]:
        bot.sendChatAction("typing")
        st = len(msg) * 0.015 - 0.5
        if st > 0:
            sleep(len(msg) * 0.015)
        bot.sendMessage(msg, use_markdown=True)
    sleep(10)
    bot.sendChatAction("typing")
    sleep(5)
    bot.sendChatAction("typing")
    sleep(5)
    msg = "Ребята, пока Грифер пошел наливать себе чай я пробрался к его компу и умоляю мне помочь! Я и есть тот самый заложник! Куда меня спрятали, я не знаю, слышал только обрывки фраз. Идите по нашим следам. Буду высылать их приметы. Спасите! Помогите!"  # noqa E501
    bot.sendMessage(msg)
    # user.set_state(state, [1])
