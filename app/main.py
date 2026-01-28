from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import pdfplumber
import tempfile
import re
from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware


from app.database import engine, SessionLocal
from app import models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





def extract_items_from_pdf(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    extracted_text = ""
    with pdfplumber.open(tmp_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

    items = []
    skip_keywords = ["gst", "invoice", "date", "total", "thank"]

    for line in extracted_text.splitlines():
        lower = line.lower()
        if any(k in lower for k in skip_keywords):
            continue

        numbers = re.findall(r"\d+\.?\d*", line)
        if len(numbers) >= 2:
            qty = int(float(numbers[0]))
            price = float(numbers[1])
            if qty > 100 or qty <= 0 or price <= 0:
                continue

            name = re.sub(r"\d+\.?\d*", "", line).strip()
            if name:
                items.append({
                    "name": name,
                    "quantity": qty,
                    "price": price
                })

    return items


@app.get("/")
def home():
    return {"status": "Expense & Profit Analyser running"}


@app.post("/upload-purchase-bill")
async def upload_purchase_bill(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    db.query(models.PurchaseItem).delete()
    db.commit()

    items = extract_items_from_pdf(file)
    for item in items:
        db.add(models.PurchaseItem(**item))

    db.commit()
    return {"message": "Purchase bill uploaded", "items_added": len(items)}


@app.post("/upload-sales-bill")
async def upload_sales_bill(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    db.query(models.SaleItem).delete()
    db.commit()

    items = extract_items_from_pdf(file)
    for item in items:
        db.add(models.SaleItem(**item))

    db.commit()
    return {"message": "Sales bill uploaded", "items_added": len(items)}


@app.get("/purchase-items")
def get_purchase_items(db: Session = Depends(get_db)):
    items = db.query(models.PurchaseItem).all()
    return [
        {"name": i.name, "quantity": i.quantity, "price": i.price}
        for i in items
    ]


@app.get("/sales-items")
def get_sales_items(db: Session = Depends(get_db)):
    items = db.query(models.SaleItem).all()
    return [
        {"name": i.name, "quantity": i.quantity, "price": i.price}
        for i in items
    ]


@app.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    total_purchase = db.query(
        func.sum(models.PurchaseItem.quantity * models.PurchaseItem.price)
    ).scalar() or 0

    total_sales = db.query(
        func.sum(models.SaleItem.quantity * models.SaleItem.price)
    ).scalar() or 0

    profit = total_sales - total_purchase

    return {
        "total_purchase": total_purchase,
        "total_sales": total_sales,
        "profit": profit
    }


@app.post("/calculate-profit")
def calculate_profit(db: Session = Depends(get_db)):
    total_purchase = db.query(
        func.sum(models.PurchaseItem.quantity * models.PurchaseItem.price)
    ).scalar() or 0

    total_sales = db.query(
        func.sum(models.SaleItem.quantity * models.SaleItem.price)
    ).scalar() or 0

    profit = total_sales - total_purchase

    history = models.ProfitHistory(
        total_purchase=total_purchase,
        total_sales=total_sales,
        profit=profit,
        created_at=datetime.utcnow()
    )

    db.add(history)
    db.commit()

    return {
        "total_purchase": total_purchase,
        "total_sales": total_sales,
        "profit": profit
    }


@app.get("/profit-history")
def profit_history(db: Session = Depends(get_db)):
    history = db.query(models.ProfitHistory).order_by(
        models.ProfitHistory.created_at.desc()
    ).all()

    return [
        {
            "total_purchase": h.total_purchase,
            "total_sales": h.total_sales,
            "profit": h.profit,
            "created_at": h.created_at
        }
        for h in history
    ]
