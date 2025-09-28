import sys

import bafser_tgapi as tgapi
from bafser import AppConfig, create_app

from bot.bot import Bot
from utils import init_db

app, run = create_app(__name__, AppConfig(DEV_MODE="dev" in sys.argv))
tgapi.setup(botCls=Bot, app=app)

DEVSERVER = "devServer" in sys.argv
if DEVSERVER:
    tgapi.set_webhook()
run(DEVSERVER, init_db)

if not DEVSERVER:
    if __name__ == "__main__":
        tgapi.run_long_polling()
    else:
        tgapi.set_webhook()
