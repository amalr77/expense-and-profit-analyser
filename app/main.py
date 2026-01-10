from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from app import models,schemas
from app.database import engine,SessionLocal

app=FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    
@app.get("/")
def home():
    return {"status": " you did it , Its working bro"}        

@app.get("/health")
def health():
    return {"status": " API working"}

@app.post("/invoices")
def create_invoice(
    invoice: schemas.InvoiceCreate,
    db: Session = Depends(get_db)
):
    db_invoice = models.Invoice(
        invoice_type=invoice.invoice_type,
        date=invoice.date
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    for item in invoice.items:
        db_item = models.InvoiceItem(
            name=item.name,
            quantity=item.quantity,
            price=item.price,
            invoice_id=db_invoice.id
        )
        db.add(db_item)

    db.commit()
    return {"message": "Invoice created", "invoice_id": db_invoice.id}
