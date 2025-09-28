import bafser_tgapi as tgapi


def reply_markup(btns: list[tuple[str, str]]):
    return tgapi.InlineKeyboardMarkup(inline_keyboard=[[
        tgapi.InlineKeyboardButton.callback(txt, data) for txt, data in btns
    ]])
