import json

from bafser import Log
from bafser_tgapi import TgUserBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from data import Roles


class User(TgUserBase):
    _default_role = Roles.user

    state: Mapped[str] = mapped_column(String(128), default="", init=False)
    state_args: Mapped[str] = mapped_column(String(256), default="", init=False)

    def set_state(self, state: str, args: list[str | int | bool] = []):
        self.state = state
        self.state_args = json.dumps(args)
        Log.updated(self, self, [
            ("state", "", self.state),
            ("state_args", "", self.state_args),
        ])

    def get_state(self) -> tuple[str, "sargs"]:
        return self.state, sargs(self.state_args)


class sargs:
    args: list[str | int | bool]

    def __init__(self, args: str):
        self.args = json.loads(args or "[]")

    def __getitem__(self, i: int):
        if i < 0 or i >= len(self.args):
            return None
        return self.args[i]
