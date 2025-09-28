from random import choice
from time import sleep
from typing import Callable

import bafser_tgapi as tgapi

from bot.bot import Bot
from bot.control import forward
from data.user import User
from utils import clear_input, reply_markup

ME = tgapi.MessageEntity
type tfn = Callable[[Bot, User], None]
_story_parts: dict[str, tfn] = {}


def answer_story(bot: Bot):
    assert bot.db_sess
    assert bot.user
    fn = _story_parts.get(bot.user.state)
    if fn:
        fn(bot, bot.user)
    else:
        forward(bot.sendMessage("ВЕЛИКА ОЩИБКА!"))


def story_part(fn: tfn):
    _story_parts[fn.__name__] = fn
    return fn


@story_part
def started(bot: Bot, user: User):
    state, args = user.get_state()
    if args[0] == 1:
        return
    user.set_state(state, [1])
    for text in [
        "Хай\\!",
        "Вот вам мой *Ультиматум*\\!!!",
        "Я вас пробил по айпи",
        "Вы меня не позвали на день рождения и теперь *пожалеете* об этом\\!",
        "Подготовил для вас подарочек \\-  *250к тонн тротила* 😂",
        "Хотите спасти свои постройки \\- найдите координаты моего тайника, в котором лежит 145 шалкеров ТНТ, а еще у меня заложник из другого измерения",  # noqa E501
        "Следуйте за вопросами, находите ответы и трепещите от страха 🤪",
    ]:
        bot.sendChatAction("typing")
        st = len(text) * 0.015 - 0.5
        if st > 0:
            sleep(len(text) * 0.015)
        forward(bot.sendMessage(text, use_markdown=True))
    bot.sendChatAction("choose_sticker")
    sleep(1)
    forward(bot.sendSticker("CAACAgEAAxUAAWjZGdMrUNNR5rRbAsVXv_X_xpZ-AAKCAgAC1jEpR2is5WGi39g8NgQ"))
    sleep(10)
    bot.sendChatAction("typing")
    sleep(5)
    bot.sendChatAction("typing")
    sleep(5)
    text = "Ребята, пока Грифер пошел наливать себе чай я пробрался к его компу и умоляю мне помочь! Я и есть тот самый заложник! Куда меня спрятали, я не знаю, слышал только обрывки фраз. Идите по нашим следам. Буду высылать их приметы. Спасите! Помогите!"  # noqa E501
    user.set_state("task1")
    forward(bot.sendMessage(text, reply_markup=reply_markup([("Вперёд!", "start_quest")])))


@story_part
def task1(bot: Bot, user: User):
    task = "Мы в любимом месте обитания уток. Сосчитайте количество качелей там."
    answers = ("7", "семь", "seven")
    run_task(bot, user, task, answers, "task2")


@story_part
def task2(bot: Bot, user: User):
    task = """
Он что\\-то подбросил в пункт Озона, заметил адрес: `Винницкая, 15`
Пароль зашифрован:
```
А \\- 1
Й \\- 1
Л \\- 1
М \\- 1
С \\- 1
```
""".strip()
    answers = ("4", "четыре", "four")
    run_task(bot, user, task, answers, "task3", use_markdown=True)


@story_part
def task3(bot: Bot, user: User):
    task = "Вижу памятник какому-то спасателю, рядом его машина. Узнайте номер машины."
    run_task(bot, user, task,
             lambda ans: ans.replace(" ", "").replace("k", "к").replace("m", "м") == "0101мкм",
             "task4")


@story_part
def task4(bot: Bot, user: User):
    task = "А вы заметили, во сколько завтракает Сытый лис?"
    answers = ("8.00", "8:00", "8 00", "8-00", "08.00", "08:00", "08 00", "08-00",
               "в восемь часов", "восемь часов", "в восемь", "в 8 часов", "8 часов")
    run_task(bot, user, task, answers, "task5")


@story_part
def task5(bot: Bot, user: User):
    task = "Вижу шар на площади. Какая же на нем актуальная для меня фраза: «Свобода не может быть…» \nЯ не успел дочитать до конца…"
    answers = ("частичной", )
    run_task(bot, user, task, answers, "task6")


@story_part
def task6(bot: Bot, user: User):
    task = "Сколько камней нужно преодолеть, чтобы борца за свободу лицезреть?"
    answers = ("6", "шесть", "six")
    run_task(bot, user, task, answers, "task7")


@story_part
def task7(bot: Bot, user: User):
    task = "Он опять пошел пить чай во «Вкусно, но не точку», что-то похожее. На здании куча шпилей. Не успел посчитать, сколько?"
    answers = ("20", "двадцать", "twenty")
    run_task(bot, user, task, answers, "task8")


@story_part
def task8(bot: Bot, user: User):
    task = "Он выделяется в воздух после дождя, а здесь висит постоянно \\- я заметил его адрес: `Раменки, д\\.6 к\\.2`\\. Сюда тоже что\\-то подбросил\\. Пароль вы уже знаете\\."  # noqa E501
    answers = ("7", "семь", "seven")
    run_task(bot, user, task, answers, "task9", use_markdown=True)


@story_part
def task9(bot: Bot, user: User):
    task = """
Зашли в какой-то странный дом. В нем подъездов больше, чем этажей! Он что-то опять подбросил в почтовый ящик.
Подъезд - перед месяцем рождения именинника
Номер ящика: возраст именинника умножить на количество дней в октябре и отнять субботу.
Код знает Принц
""".strip()
    answers = ("1", "один", "one")
    run_task(bot, user, task, answers, "task10")


@story_part
def task10(bot: Bot, user: User):
    task = "Теперь он здорово проголодался и ищет, где поесть. Нашел какой-то ресторан со странным названием типа «чая больше нет». Поторопитесь и спасите меня наконец! Когда найдете это место, введите весь код целиком. "  # noqa E501
    answers = ("471", "четыре семь один", "четыреста семьдесять один")
    run_task(bot, user, task, answers, "quest_end")


@story_part
def quest_end(bot: Bot, user: User):
    state, args = user.get_state()
    if args[0] == 1:
        return
    user.set_state(state, [1])
    msg = "Ура, мне повезло! Здесь добрая фея с приметами мамы именинника, и она  заметила что-то подозрительное. Надеюсь, что скоро вы меня спасете! Мы поднимались по лестнице, кажется, на второй этаж."  # noqa E501
    forward(bot.sendMessage(msg))
    forward(bot.sendMessage("Осторожно, здание заминировано!"))


def run_task(bot: Bot, user: User, task: str, answers: tuple[str, ...] | Callable[[str], bool], next_state: str, *,
             use_markdown: bool = False):
    state, args = user.get_state()
    if args[0] is None:
        user.set_state(state, [1])
        send_backvoice(bot)
        forward(bot.sendMessage(task, use_markdown=use_markdown, reply_markup=reply_markup([("Подсказка", "task_hint 0")])))
        return
    if not bot.message:
        return
    answer = clear_input(bot.message.text)
    if callable(answers) and answers(answer) or \
            isinstance(answers, tuple) and answer in answers:
        forward(bot.sendMessage("Верно!"))
        user.set_state(next_state)
        answer_story(bot)
    else:
        send_you_are_wrong(bot)


def send_backvoice(bot: Bot):
    p1 = "Голос свыше:\n"
    p2 = "Убедись, что твои друзья рядом и слышат тебя."
    msg = p1 + p2
    forward(bot.sendMessage(msg, entities=[ME.italic(0, ME.len(p1)), ME.blockquote(ME.len(p1), ME.len(p2))]))


def send_you_are_wrong(bot: Bot):
    forward(bot.sendMessage(choice([
        "Думаю, стоит подумать ещё", "Мимо!", "Не подходит", "Не угадал!", "Неа!", "Неверная догадка",
        "Неверно!", "Неверное решение", "Неправильный ответ!", "Нет, не то", "Нет, не угадал", "Нет, неверно",
        "Нет, это неправильный вариант", "Нет-нет-нет", "Ну же, подумай лучше!", "Ну нет, это не то",
        "Ну-ну, не то", "Ответ неверный", "Ошибочка!", "Подумай ещё!", "Пока неверно", "Попробуй ещё вариант",
        "Попробуй иначе", "Попробуй по-другому", "Попробуй снова!", "Провал!", "Промах!", "Увы, неправильно",
        "Увы, нет!", "Увы, ошибка", "Что-то не похоже на ответ", "Это не то, что нужно", "Это ошибка",
    ])))
