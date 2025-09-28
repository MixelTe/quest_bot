import re

reg1 = re.compile("[^0-9a-zA-Zа-яА-ЯёЁ \t\n]+")
reg2 = re.compile("[ \t\n]+")


def clear_input(inp: str):
    return reg2.sub(" ", reg1.sub("", inp.strip())).lower()
