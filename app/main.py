
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models

app = FastAPI(
    title="KYC Evidence & Review Management System",
    description="API for KYC onboarding, evidence, risk and reviews",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "KYC Evidence & Review Management System",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/customers")
def get_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    customers = (
        db.query(models.Customer)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        {
            "customer_id": c.customer_id,
            "full_name": c.full_name,
            "email": c.email,
            "onboarding_status": c.onboarding_status,
            "customer_type_id": c.customer_type_id
        }
        for c in customers
    ]


@app.get("/customers/{customer_id}")
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    customer = db.query(models.Customer).filter_by(
        customer_id=customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "customer_id": customer.customer_id,
        "full_name": customer.full_name,
        "email": customer.email,
        "onboarding_status": customer.onboarding_status,
        "customer_type_id": customer.customer_type_id
    }
@app.get("/customers/{customer_id}/documents")
def get_customer_documents(
    customer_id: str,
    db: Session = Depends(get_db)
):
    customer = db.query(models.Customer).filter_by(
        customer_id=customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    documents = db.query(models.Document).filter_by(
        customer_id=customer_id
    ).all()

    return [
        {
            "document_id": d.document_id,
            "document_type": d.document_type,
            "issue_date": d.issue_date,
            "expiry_date": d.expiry_date,
            "document_status": d.document_status,
            "holder_name": d.holder_name
        }
        for d in documents
    ]