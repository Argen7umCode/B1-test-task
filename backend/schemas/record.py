from pydantic import BaseModel


class IncomingBalanse(BaseModel):
    in_active_balance: float
    in_passive_balance: float

class OutcomingBalanse(BaseModel):
    out_active_balance: float
    out_passive_balance: float

class RecordSchema(IncomingBalanse):
    class_name: str
    unid: int

class RecordSchemaResponse(RecordSchema):
    debit: float
    credit: float

class RecordSchemaWithOutputBalancesResponse(RecordSchemaResponse, 
                                             OutcomingBalanse):
    pass