from datetime import date

import pytest

from app.database import SessionLocal
from app.models import (
    Customer,
    Document,
    ReviewCase,
    BeneficialOwner,
    KYCRequirement
)

TODAY = date(2026, 11, 10)


@pytest.fixture
def session():
    db = SessionLocal()
    yield db
    db.close()


def test_customers_exist(session):
    assert session.query(Customer).count() >= 100


def test_documents_exist(session):
    assert session.query(Document).count() >= 250


def test_all_documents_have_customers(session):
    customers = {
        c.customer_id
        for c in session.query(Customer).all()
    }

    documents = session.query(Document).all()

    assert all(d.customer_id in customers for d in documents)


def test_expired_verified_document_exists(session):
    documents = session.query(Document).all()

    assert any(
        d.expiry_date is not None
        and d.expiry_date < TODAY
        and d.document_status == "VERIFIED"
        for d in documents
    )


def test_approved_customer_missing_evidence(session):
    customers = session.query(Customer).filter_by(
        onboarding_status="APPROVED"
    ).all()

    requirements = session.query(KYCRequirement).filter_by(
        is_mandatory=True
    ).all()

    documents = session.query(Document).all()

    found = False

    for customer in customers:
        required = {
            r.document_type
            for r in requirements
            if r.customer_type_id == customer.customer_type_id
        }

        available = {
            d.document_type
            for d in documents
            if d.customer_id == customer.customer_id
            and d.document_status == "VERIFIED"
        }

        if required - available:
            found = True

    assert found


def test_ownership_above_100_exists(session):
    owners = session.query(BeneficialOwner).all()

    totals = {}

    for owner in owners:
        totals[owner.customer_id] = (
            totals.get(owner.customer_id, 0)
            + owner.ownership_percentage
        )

    assert any(total > 100 for total in totals.values())


def test_closed_review_without_resolution_exists(session):
    reviews = session.query(ReviewCase).all()

    assert any(
        r.review_status == "CLOSED" and not r.resolution
        for r in reviews
    )


def test_overdue_review_exists(session):
    reviews = session.query(ReviewCase).all()

    assert any(
        r.due_date < TODAY and r.review_status != "CLOSED"
        for r in reviews
    )