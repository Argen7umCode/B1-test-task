from pydantic import BaseModel


class RecordSchema(BaseModel):
    unid: int
    input_balance_id: int
    turnover_id: int
    payment_classid: int