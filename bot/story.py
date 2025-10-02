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
        "Вот вам мой *Ультиматум*\\!\\!\\!",
        "Я вас пробил по айпи",
        "Вы меня не позвали на день рождения и теперь *пожалеете* об этом\\!",
        "Подготовил для вас подарочек \\-  *250к тонн тротила* 😂 Они спрятаны в тайнике до 14:00\\. А потом \\- все, всему конец\\!",
        "Хотите спасти свои постройки \\- найдите координаты моего тайника, в котором лежит 145 шалкеров ТНТ, а еще у меня заложник из другого измерения",  # noqa E501
        "Ищите как хотите и трепещите от страха\\! Ха\\-ха\\! 🤪",
    ]:
        bot.sendChatAction("typing")
        st = len(text) * 0.02 - 0.25
        if st > 0:
            sleep(st)
        forward(bot.sendMessage(text, use_markdown=True))
    bot.sendChatAction("choose_sticker")
    sleep(1)
    forward(bot.sendSticker("CAACAgEAAxUAAWjZGdMrUNNR5rRbAsVXv_X_xpZ-AAKCAgAC1jEpR2is5WGi39g8NgQ"))
    sleep(15)
    bot.sendChatAction("typing")
    sleep(5)
    bot.sendChatAction("typing")
    sleep(5)
    text = "Ребята, пока Грифер пошел наливать себе чай я пробрался к его компу и умоляю мне помочь! Я и есть тот самый заложник! Куда меня спрятали, я не знаю, слышал только обрывки фраз. Идите по нашим следам. Буду высылать их приметы. Спасите! Помогите!"  # noqa E501
    forward(bot.sendMessage(text, reply_markup=reply_markup([("Вперёд!", "start_quest")])))


@story_part
def task1(bot: Bot, user: User):
    task = "Мы в любимом  месте обитания уток. Зачем-то он посчитал здесь все качели. Посчитайте и вы на всякий случай."
    answers = ("7", "семь", "seven")
    ok_phrase = ["О, вижу цифру", "Здорово, что вы взялись меня спасать!"]
    run_task(bot, user, task, answers, ok_phrase, "task2")


@story_part
def task2(bot: Bot, user: User):
    task = """
Он что\\-то подбросил в пункт Озона, заметил адрес: `Винницкая, 15`\\. Сказал сотрудникам какой\\-то пароль\\.
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
    ok_phrase = ["О, вижу цифру", "Я сам не понял, как тут оказался. Когда я сюда попал, оказалось, что все имеют углы, и я тоже начинаю заугляться…"]
    run_task(bot, user, task, answers, ok_phrase, "task3", use_markdown=True)


@story_part
def task3(bot: Bot, user: User):
    task = "Вижу памятник какому-то спасателю, рядом его машина. Он записал номер машины. Наверное, и вам пригодится."
    answers = lambda ans: ans.replace(" ", "").replace("-", "").replace(".", "").replace("k", "к").replace("m", "м") == "0101мкм"
    ok_phrase = ["Вижу, вы нашли то, что надо", "А я ведь тоже шел на день рождения. Но меня поймал Грифер и держит у себя взаперти."]
    run_task(bot, user, task, answers, ok_phrase, "task4")


@story_part
def task4(bot: Bot, user: User):
    task = "Он пошел чистить зубы после завтрака. А вы заметили, во сколько завтракает Сытый лис?"
    answers = ("8.00", "8:00", "8 00", "8-00", "08.00", "08:00", "08 00", "08-00",
               "в восемь часов", "восемь часов", "в восемь", "в 8 часов", "8 часов")
    ok_phrase = ["Верно", "Говорят, в Майнкрафте можно не завтракать. Какой ужас!"]
    run_task(bot, user, task, answers, ok_phrase, "task5")


@story_part
def task5(bot: Bot, user: User):
    task = "Вижу шар на площади. Какая же на нем актуальная для меня фраза: «Свобода не может быть…» \nЯ не успел дочитать до конца…"
    answers = ("частичной", )
    ok_phrase = ["Да, точно! Именно так!"]
    run_task(bot, user, task, answers, ok_phrase, "task6")


@story_part
def task6(bot: Bot, user: User):
    task = "Он ушел стричь ногти. Но сначала посчитал, сколько камней нужно преодолеть, чтобы борца за свободу лицезреть."
    answers = ("6", "шесть", "six")
    ok_phrase = ["Хорошо, я запомню", "Представляете, я тут узнал, что оказывается, крипер раньше был свиньей"]
    run_task(bot, user, task, answers, ok_phrase, "task7")


@story_part
def task7(bot: Bot, user: User):
    task = "Он опять пошел пить чай во «Вкусно, но не точку», что-то похожее. На здании куча шпилей. Зачем-то их все посчитал. Вы тоже так можете."
    answers = ("20", "двадцать", "twenty")
    ok_phrase = ["Пойдет!", "А я тут узнал, что оказывается, раньше в Майнкрафте кровати были только красные."]
    run_task(bot, user, task, answers, ok_phrase, "task8")


@story_part
def task8(bot: Bot, user: User):
    task = "Этот газ выделяется в воздух после дождя, а здесь висит постоянно \\- я заметил его адрес:  `Раменки, д\\.6 к\\.2`\\. Сюда Грифер тоже что\\-то подбросил\\. Пароль вы уже знаете\\."  # noqa E501
    answers = ("7", "семь", "seven")
    ok_phrase = ["Вижу цифру. Пригодится, наверное."]
    run_task(bot, user, task, answers, ok_phrase, "task9", use_markdown=True)


@story_part
def task9(bot: Bot, user: User):
    task = """
Зашли в какой-то странный дом. В нем подъездов больше, чем этажей! Он что-то опять подбросил в почтовый ящик.
Подъезд - перед месяцем рождения именинника
Номер ящика: возраст именинника умножить на количество дней в октябре и отнять субботу.
Код знает Принц
""".strip()
    answers = ("1", "один", "one")
    ok_phrase = ["Еще цифра появилась. Наверное, важная."]
    run_task(bot, user, task, answers, ok_phrase, "task10")


@story_part
def task10(bot: Bot, user: User):
    task = "Теперь он здорово проголодался и ищет, где поесть. Нашел какой-то ресторан со странным названием типа «чая больше нет». Поторопитесь и спасите меня наконец! Когда найдете это место, введите весь код целиком, я впишу в командный блок код и ваши имена в вайт лист."  # noqa E501
    answers = ("471", "четыре семь один", "четыреста семьдесять один")
    ok_phrase = ["Код получил. Вы молодцы! Мое спасение близко!"]
    run_task(bot, user, task, answers, ok_phrase, "quest_end")


@story_part
def quest_end(bot: Bot, user: User):
    state, args = user.get_state()
    if args[0] == 1:
        return
    user.set_state(state, [1])
    msg = "Ура, мне повезло! Здесь добрая фея с приметами мамы именинника, и она заметила что-то подозрительное. Надеюсь, что скоро вы меня спасете! Мы поднимались по лестнице, кажется, на второй этаж."  # noqa E501
    forward(bot.sendMessage(msg))

    bot.sendChatAction("typing")
    sleep(0.5)
    msg = "Караул! Он заметил, что я вам помогаю! Зачем ему поршень? И откуда у него бедрок?"
    forward(bot.sendMessage(msg))

    sleep(1)
    bot.sendChatAction("typing")
    sleep(0.5)
    msg = "Ха-ха-ха! Этот мерзкий тип вам подсказывал, и за это я засунул его прямо в бедрок. 🤣 И теперь здание заминиро"
    forward(bot.sendMessage(msg))


def run_task(bot: Bot, user: User, task: str, answers: tuple[str, ...] | Callable[[str], bool], ok_phrase: list[str], next_state: str, *,
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
        for msg in ok_phrase:
            bot.sendChatAction("typing")
            sleep(0.25)
            forward(bot.sendMessage(msg))
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
        "Не подходит", "Неа!", "Ой-ой-ой!", "Провал!", "Промах!",
        "Что-то не похоже на ответ", "Ушами чую, неправильный ответ", "Готов поспорить, нужно еще подумать",
        "Боюсь, это не так", "Такие себе мальчики", "Не очень мальчики",
    ])))
