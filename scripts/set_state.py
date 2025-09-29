import sys

import bafser_tgapi as tgapi
from bafser import db_session

from data.user import User


def run(state: str, dev: bool):
    tgapi.setup(dev=dev)
    db_session.global_init(dev)
    db_sess = db_session.create_session()
    print(f"set state: {state}")
    for player in User.get_all_players(db_sess):
        print(f"\tfor {player.get_username()} ({player.get_tagname()})")
        player.set_state(state)
    db_sess.close()


if __name__ == "__main__":
    if len(sys.argv) == 2 or (len(sys.argv) == 3 and sys.argv[-1] == "dev"):
        run(sys.argv[1], sys.argv[-1] == "dev")
    else:
        print("set_state.py state [dev]")
