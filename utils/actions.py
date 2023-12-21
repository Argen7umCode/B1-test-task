from typing import List, Tuple
import pandas as pd
from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from pprint import pprint

from dal import DAL
from db.models import PaymentClass, Record
from schemas.record import RecordSchemaResponse, RecordSchemaWithOutputBalancesResponse


async def process_class(payment_class_description: str, 
                        df: pd.DataFrame, 
                        session: AsyncSession) -> List[RecordSchemaResponse]:
    async with session.begin():
        dal = DAL(session)

        payment_class_select_query = select(PaymentClass)\
                .where(PaymentClass.description == payment_class_description)
        payment_class = await dal.make_query_and_get_one(payment_class_select_query)
        
        if payment_class is None:
            payment_class = PaymentClass(description=payment_class_description)
            await dal.add_one(payment_class)
        
        to_return = []
        to_add = []
        for row in df[['unid', 'active', 'passive', 'debit', 'credit']].to_numpy():
            unid, active, passive, debit, credit = row
            record = Record(
                        unid=int(unid), 
                        active=active,
                        passive=passive,
                        debit=debit,
                        credit=credit,
                        payment_class=payment_class
                    )
            to_add.append(record)
            to_return.append(
                RecordSchemaResponse(
                    class_name=payment_class_description,
                    unid=int(unid),
                    in_active_balance=active,
                    in_passive_balance=passive,
                    debit=debit,
                    credit=credit,
                )
            )
        await dal.add_all(to_add)
    return to_return


def get_outcoming_acitve_balance(in_active: float, 
                                 debit: float, 
                                 credit: float) -> float:
    return in_active + debit - credit if in_active != 0 else 0

def get_outcoming_passive_balance(in_passive: float, 
                                  debit: float, 
                                  credit: float) -> float:
    return  in_passive - debit + credit if in_passive != 0 else 0

def get_outcoming_balance(in_active: float,
                          in_passive: float, 
                          debit: float,
                          credit: float) -> Tuple[float]:
    return (get_outcoming_acitve_balance(in_active, debit, credit),    
            get_outcoming_passive_balance(in_passive, debit, credit))


async def get_records_from_db(session: AsyncSession) \
                                 -> List[RecordSchemaWithOutputBalancesResponse]:
    async with session.begin():
        dal = DAL(session)

        select_query = select(Record, PaymentClass).join(PaymentClass).distinct(Record.unid)
        records = await dal.make_query_and_get_all(select_query)
    
        to_return = []
        for record in records:
            record = record[0]
            out_active, out_passive = get_outcoming_balance(
                in_active=record.active,
                in_passive=record.passive,
                debit=record.debit,
                credit=record.credit
            )

            record_to_return = RecordSchemaWithOutputBalancesResponse(
                unid=record.unid,
                in_active_balance=record.active,
                in_passive_balance=record.passive,
                debit=record.debit,
                credit=record.credit,
                out_active_balance=out_active,
                out_passive_balance=out_passive,
                class_name=record.payment_class.description
            )
            to_return.append(record_to_return)
    return to_return
    
