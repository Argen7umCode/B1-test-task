from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base


Base = declarative_base()



class Class(Base):
    __tablename__ = "class"
    class_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False, unique=True)

    records: Mapped[List['Record']] = relationship('Records', back_populates='class', lazy="selectin")


class InputBalance(Base):
    __tablename__ = "input_balance"
    input_balance_id: Mapped[int] = mapped_column(primary_key=True)
    active: Mapped[float] = mapped_column(nullable=False, unique=True)
    passive: Mapped[float] = mapped_column(nullable=False, unique=True)
    
    record: Mapped['Record'] = relationship('Records', back_populates='inputbalance', uselist=False, lazy="selectin")


class Turnover(Base):
    __tablename__ = "turnover"
    turnover_id: Mapped[int] = mapped_column(primary_key=True)
    debit: Mapped[float] = mapped_column(nullable=False, unique=True)
    credit: Mapped[float] = mapped_column(nullable=False, unique=True)
    
    record: Mapped['Record'] = relationship('Records', back_populates='turnover', uselist=False, lazy="selectin")


class Record(Base):
    __tablename__ = "record"
    record_id:        Mapped[int] = mapped_column(primary_key=True)
    unid:             Mapped[int] = mapped_column(nullable=False)
    input_balance_id: Mapped[int] = mapped_column(ForeignKey('input_balance.input_balance_id'))
    turnover_id:      Mapped[int] = mapped_column(ForeignKey('turnover.turnover_id'))
    class_id:         Mapped[int] = mapped_column(ForeignKey('class.class_id'))

    input_balance:    Mapped[int] = relationship('InputBalanse', back_populates='record', lazy="selectin")
    turnover:         Mapped[int] = relationship('Turnover', back_populates='record', lazy="selectin")
    class_:           Mapped[int] = relationship('Class', back_populates='record', lazy="selectin")