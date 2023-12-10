from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base

from db import Base


Base = declarative_base()

class Class(Base):
    __tablename__ = "class"
    class_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False, unique=True)

    records: Mapped[List['Record']] = relationship()


class InputBalance(Base):
    __tablename__ = "input_balance"
    input_balance_id: Mapped[int] = mapped_column(primary_key=True)
    active: Mapped[float] = mapped_column(nullable=False, unique=True)
    passive: Mapped[float] = mapped_column(nullable=False, unique=True)
    
    records: Mapped[List['Record']] = relationship()


class Turnover(Base):
    __tablename__ = "turnover"
    turnover_id: Mapped[int] = mapped_column(primary_key=True)
    debit: Mapped[float] = mapped_column(nullable=False, unique=True)
    credit: Mapped[float] = mapped_column(nullable=False, unique=True)
    
    records: Mapped[List['Record']] = relationship()


class Record(Base):
    __tablename__ = "record"
    record_id:        Mapped[int] = mapped_column(primary_key=True)
    input_balance_id: Mapped[int] = mapped_column(ForeignKey('input_balance.input_balance_id'))
    turnover_id:      Mapped[int] = mapped_column(ForeignKey('turnover.class_id'))
    class_id:         Mapped[int] = mapped_column(ForeignKey('class.class_id'))
