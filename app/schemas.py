from pydantic import BaseModel
from datetime import date
from typing import List

class InvoiceItemCreate(BaseModel):
    name: str
    quantity: int
    price: float

class InvoiceCreate(BaseModel):
    invoice_type: str
    date: date
    items: List[InvoiceItemCreate]
