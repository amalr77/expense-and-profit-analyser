from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
import pdfplumber
import tempfile
import re
from app import models, schemas
from app.database import engine, SessionLocal
from datetime import date

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"status": "you did it, it's working bro"}


def parse_invoice_text(text: str):
    items = []
    lines = text.splitlines()

    skip_keywords = ["gst", "invoice", "date", "total", "thank"]

    for line in lines:
        lower_line = line.lower()

        # Skip obvious non-item lines
        if any(keyword in lower_line for keyword in skip_keywords):
            continue

        numbers = re.findall(r"\d+\.?\d*", line)

        if len(numbers) >= 2:
            qty = int(float(numbers[0]))
            price = float(numbers[1])

           
            if qty > 100:
                continue

            name = re.sub(r"\d+\.?\d*", "", line).strip()

            if name and qty > 0 and price > 0:
                items.append({
                    "name": name,
                    "quantity": qty,
                    "price": price
                })

    return items

@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported"}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    extracted_text = ""
    with pdfplumber.open(tmp_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"

    parsed_items = parse_invoice_text(extracted_text)

    # 🔑 CREATE INVOICE IN DB
    db_invoice = models.Invoice(
        invoice_type="purchase",
        date=date.today()
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    for item in parsed_items:
        db_item = models.InvoiceItem(
            name=item["name"],
            quantity=item["quantity"],
            price=item["price"],
            invoice_id=db_invoice.id
        )
        db.add(db_item)

    db.commit()

    return {
        "message": "Invoice created from PDF",
        "invoice_id": db_invoice.id,
        "items_saved": len(parsed_items)
    }
