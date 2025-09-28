from __future__ import annotations

from typing import Optional

from bafser import Log, SingletonMixin, SqlAlchemyBase
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from data._tables import Tables
from data.user import User


class Config(SqlAlchemyBase, SingletonMixin):
    __tablename__ = Tables.Config

    control_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger, init=False)
    control_chat_thread_id: Mapped[Optional[int]] = mapped_column(init=False)
    broadcast_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger, init=False)
    broadcast_chat_thread_id: Mapped[Optional[int]] = mapped_column(init=False)

    def set_control_chat(self, actor: User, chat_id: int, chat_thread_id: int | None):
        self.control_chat_id = chat_id
        self.control_chat_thread_id = chat_thread_id
        Log.updated(self, actor, [
            ("control_chat_id", "", chat_id),
            ("control_chat_thread_id", "", chat_thread_id),
        ])

    def set_broadcast_chat(self, actor: User, chat_id: int, chat_thread_id: int | None):
        self.broadcast_chat_id = chat_id
        self.broadcast_chat_thread_id = chat_thread_id
        Log.updated(self, actor, [
            ("broadcast_chat_id", "", chat_id),
            ("broadcast_chat_thread_id", "", chat_thread_id),
        ])
