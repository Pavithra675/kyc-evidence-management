
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
@app.get("/customers/{customer_id}/risk")
def get_customer_risk(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter_by(customer_id=customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    risk = db.query(models.RiskRating).filter_by(customer_id=customer_id).first()
    if not risk:
        raise HTTPException(status_code=404, detail="Risk rating not found")

    return {
        "risk_id": risk.risk_id,
        "customer_id": risk.customer_id,
        "risk_level": risk.risk_level,
        "risk_score": risk.risk_score,
        "assessed_at": risk.assessed_at
    }


@app.get("/customers/{customer_id}/reviews")
def get_customer_reviews(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter_by(customer_id=customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    reviews = db.query(models.ReviewCase).filter_by(customer_id=customer_id).all()
    return [
        {
            "review_id": r.review_id,
            "customer_id": r.customer_id,
            "review_date": r.review_date,
            "due_date": r.due_date,
            "review_status": r.review_status,
            "resolution": r.resolution
        }
        for r in reviews
    ]


@app.get("/customers/{customer_id}/beneficial-owners")
def get_beneficial_owners(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter_by(customer_id=customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    owners = db.query(models.BeneficialOwner).filter_by(customer_id=customer_id).all()
    return [
        {
            "owner_id": o.owner_id,
            "customer_id": o.customer_id,
            "owner_name": o.owner_name,
            "ownership_percentage": o.ownership_percentage
        }
        for o in owners
    ]


@app.get("/customers/{customer_id}/alerts")
def get_customer_alerts(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter_by(customer_id=customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    alerts = db.query(models.Alert).filter_by(customer_id=customer_id).all()
    return [
        {
            "alert_id": a.alert_id,
            "customer_id": a.customer_id,
            "alert_type": a.alert_type,
            "alert_message": a.alert_message,
            "created_at": a.created_at,
            "alert_status": a.alert_status
        }
        for a in alerts
    ]


@app.get("/documents/{document_id}/verifications")
def get_document_verifications(document_id: str, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter_by(document_id=document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    verifications = db.query(models.Verification).filter_by(document_id=document_id).all()
    return [
        {
            "verification_id": v.verification_id,
            "document_id": v.document_id,
            "verification_status": v.verification_status,
            "verified_at": v.verified_at,
            "reviewer": v.reviewer
        }
        for v in verifications
    ]


@app.get("/reviews")
def get_all_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = db.query(models.ReviewCase).offset(skip).limit(limit).all()
    return [
        {
            "review_id": r.review_id,
            "customer_id": r.customer_id,
            "review_date": r.review_date,
            "due_date": r.due_date,
            "review_status": r.review_status,
            "resolution": r.resolution
        }
        for r in reviews
    ]


@app.get("/kyc-requirements")
def get_kyc_requirements(db: Session = Depends(get_db)):
    requirements = db.query(models.KYCRequirement).all()
    return [
        {
            "requirement_id": r.requirement_id,
            "customer_type_id": r.customer_type_id,
            "document_type": r.document_type,
            "risk_level": r.risk_level,
            "is_mandatory": r.is_mandatory
        }
        for r in requirements
    ]


@app.get("/audit-events")
def get_audit_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = (
        db.query(models.AuditEvent)
        .order_by(models.AuditEvent.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {
            "event_id": e.event_id,
            "entity_type": e.entity_type,
            "entity_id": e.entity_id,
            "event_type": e.event_type,
            "old_value": e.old_value,
            "new_value": e.new_value,
            "reason": e.reason,
            "actor": e.actor,
            "created_at": e.created_at
        }
        for e in events
    ]


@app.get("/customers/{customer_id}/kyc-completeness")
def get_kyc_completeness(
    customer_id: str,
    db: Session = Depends(get_db)
):
    from datetime import date

    customer = db.query(models.Customer).filter_by(
        customer_id=customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    requirements = db.query(models.KYCRequirement).filter_by(
        customer_type_id=customer.customer_type_id,
        is_mandatory=True
    ).all()

    results = []

    for requirement in requirements:
        documents = db.query(models.Document).filter_by(
            customer_id=customer_id,
            document_type=requirement.document_type
        ).all()

        requirement_status = "MISSING"
        selected_document_id = None

        for document in documents:
            verification = db.query(
                models.Verification
            ).filter_by(
                document_id=document.document_id
            ).first()

            verification_status = (
                verification.verification_status.upper()
                if verification else None
            )

            document_status = document.document_status.upper()

            if (
                document_status == "VERIFIED"
                and verification_status == "APPROVED"
                and (
                    document.expiry_date is None
                    or document.expiry_date >= date.today()
                )
            ):
                requirement_status = "SATISFIED"
                selected_document_id = document.document_id
                break

            if (
                document.expiry_date is not None
                and document.expiry_date < date.today()
            ):
                requirement_status = "EXPIRED"
                selected_document_id = document.document_id

            elif (
                document_status == "PENDING"
                or verification_status == "PENDING"
            ):
                if requirement_status not in ["EXPIRED"]:
                    requirement_status = "PENDING"
                    selected_document_id = document.document_id

            elif (
                document_status == "REJECTED"
                or verification_status == "REJECTED"
            ):
                if requirement_status not in ["EXPIRED", "PENDING"]:
                    requirement_status = "REJECTED"
                    selected_document_id = document.document_id

            elif requirement_status == "MISSING":
                requirement_status = "UNVERIFIED"
                selected_document_id = document.document_id

        results.append({
            "requirement_id": requirement.requirement_id,
            "document_type": requirement.document_type,
            "required_risk_level": requirement.risk_level,
            "status": requirement_status,
            "document_id": selected_document_id
        })

    total = len(results)
    satisfied = sum(
        1 for item in results
        if item["status"] == "SATISFIED"
    )

    percentage = round(
        (satisfied / total) * 100, 2
    ) if total else 100.0

    return {
        "customer_id": customer_id,
        "customer_type": customer.customer_type.type_name,
        "total_mandatory_requirements": total,
        "satisfied_requirements": satisfied,
        "incomplete_requirements": total - satisfied,
        "completeness_percentage": percentage,
        "all_mandatory_evidence_complete": satisfied == total,
        "requirements": results
    }


@app.post("/alerts/check-expiring-documents")
def check_expiring_documents(
    warning_days: int = 30,
    db: Session = Depends(get_db)
):
    from datetime import date, datetime, timedelta

    if warning_days < 1 or warning_days > 365:
        raise HTTPException(
            status_code=400,
            detail="warning_days must be between 1 and 365"
        )

    today = date.today()
    warning_date = today + timedelta(days=warning_days)

    documents = db.query(models.Document).filter(
        models.Document.expiry_date >= today,
        models.Document.expiry_date <= warning_date
    ).all()

    existing_alerts = db.query(models.Alert).filter_by(
        alert_type="DOCUMENT_EXPIRING_SOON"
    ).all()

    existing_messages = {
        alert.alert_message for alert in existing_alerts
    }

    all_alerts = db.query(models.Alert.alert_id).all()
    max_number = 0

    for (alert_id,) in all_alerts:
        try:
            number = int(alert_id.rsplit("-", 1)[-1])
            max_number = max(max_number, number)
        except ValueError:
            continue

    created_alerts = []

    for document in documents:
        message = (
            f"Document {document.document_id} "
            f"will expire on {document.expiry_date}."
        )

        if message in existing_messages:
            continue

        max_number += 1

        alert = models.Alert(
            alert_id=f"ALT-{max_number:06d}",
            customer_id=document.customer_id,
            alert_type="DOCUMENT_EXPIRING_SOON",
            alert_message=message,
            created_at=datetime.now(),
            alert_status="OPEN"
        )

        db.add(alert)
        created_alerts.append({
            "alert_id": alert.alert_id,
            "document_id": document.document_id,
            "customer_id": document.customer_id,
            "expiry_date": document.expiry_date
        })

        existing_messages.add(message)

    db.commit()

    return {
        "warning_period_days": warning_days,
        "documents_checked": len(documents),
        "new_alerts_created": len(created_alerts),
        "alerts": created_alerts
    }

