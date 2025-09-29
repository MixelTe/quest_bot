import bafser_tgapi as tgapi

type text = str
type cmd = str


def reply_markup(*btns: list[tuple[text, cmd]]):
    return tgapi.InlineKeyboardMarkup(inline_keyboard=[[
        tgapi.InlineKeyboardButton.callback(txt, data) for txt, data in row
    ] for row in btns])
