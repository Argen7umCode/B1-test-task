from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PaymentClass(Base):
    __tablename__ = "payment_class"
    payment_class_id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False, unique=True)
    records = relationship('Record', back_populates='payment_class')

class Record(Base):
    __tablename__ = "record"
    record_id = Column(Integer, primary_key=True)
    unid = Column(Integer, nullable=False)
    active = Column(Float, nullable=False)
    passive = Column(Float, nullable=False)
    debit = Column(Float, nullable=False)
    credit = Column(Float, nullable=False)
    payment_class_id = Column(Integer, ForeignKey('payment_class.payment_class_id'))

    payment_class = relationship('PaymentClass', back_populates='records')

