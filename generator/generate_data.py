import random
import argparse
from datetime import datetime, date, timedelta

from app.database import engine, SessionLocal, Base
from app.models import (
    CustomerType, KYCRequirement, Customer, RiskRating,
    Document, Verification, ReviewCase, BeneficialOwner,
    Alert, AuditEvent
)

SEED = 20261022
TODAY = date(2026, 11, 10)


FIRST_NAMES = [
    "Aarav", "Ananya", "Rahul", "Priya", "Arjun",
    "Sneha", "Kiran", "Meera", "Rohan", "Divya",
    "Aditya", "Neha", "Vikram", "Pooja", "Sanjay"
]

LAST_NAMES = [
    "Sharma", "Reddy", "Kumar", "Patel", "Rao",
    "Singh", "Gupta", "Nair", "Verma", "Das"
]


def generate_master_data(session):
    session.add_all([
        CustomerType(
            customer_type_id="TYPE-001",
            type_name="Individual"
        ),
        CustomerType(
            customer_type_id="TYPE-002",
            type_name="Business"
        )
    ])

    rules = {
        "TYPE-001": [
            ("IDENTITY", "LOW"),
            ("ADDRESS", "LOW"),
            ("INCOME", "MEDIUM"),
            ("SOURCE_OF_FUNDS", "HIGH")
        ],
        "TYPE-002": [
            ("INCORPORATION", "LOW"),
            ("ADDRESS", "LOW"),
            ("OWNERSHIP", "LOW"),
            ("DIRECTORS", "MEDIUM"),
            ("SOURCE_OF_FUNDS", "HIGH")
        ]
    }

    counter = 1

    for type_id, requirements in rules.items():
        for document_type, risk_level in requirements:
            session.add(
                KYCRequirement(
                    requirement_id=f"KYC-{counter:06d}",
                    customer_type_id=type_id,
                    document_type=document_type,
                    risk_level=risk_level,
                    is_mandatory=True
                )
            )
            counter += 1

    session.commit()
    print("Master data generated.")


def generate_customers(session, total_customers):
    risk_levels = ["LOW", "MEDIUM", "HIGH"]

    for i in range(1, total_customers + 1):
        customer_id = f"CUS-{i:06d}"

        is_business = (i % 8 == 0)

        customer_type_id = (
            "TYPE-002" if is_business else "TYPE-001"
        )

        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)

        full_name = (
            f"{last} Technologies Pvt Ltd"
            if is_business else f"{first} {last}"
        )

        # Special edge case:
        # This approved customer will have no documents.
        onboarding_status = (
            "APPROVED" if i == 3 else "PENDING"
        )

        session.add(
            Customer(
                customer_id=customer_id,
                customer_type_id=customer_type_id,
                full_name=full_name,
                email=f"customer{i:06d}@example.com",
                onboarding_status=onboarding_status,
                created_at=datetime(2026, 1, 1)
            )
        )

        risk_level = random.choice(risk_levels)

        risk_score = {
            "LOW": random.uniform(0, 30),
            "MEDIUM": random.uniform(31, 70),
            "HIGH": random.uniform(71, 100)
        }[risk_level]

        session.add(
            RiskRating(
                risk_id=f"RISK-{i:06d}",
                customer_id=customer_id,
                risk_level=risk_level,
                risk_score=round(risk_score, 2),
                assessed_at=datetime(2026, 1, 1)
            )
        )

    session.commit()
    print("Customers generated:", total_customers)


def generate_documents(session, total_documents):
    customers = session.query(Customer).order_by(
        Customer.customer_id
    ).all()

    document_counter = {
        c.customer_id: 0 for c in customers
    }

    verification_counter = 1
    audit_counter = 1
    duplicate_template = None

    generated = 0
    customer_index = 0

    while generated < total_documents:
        customer = customers[
            customer_index % len(customers)
        ]
        customer_index += 1

        # CUS-000003 is intentionally left without documents.
        if customer.customer_id == "CUS-000003":
            continue

        document_counter[customer.customer_id] += 1
        doc_number = document_counter[customer.customer_id]

        if customer.customer_type_id == "TYPE-001":
            document_types = [
                "IDENTITY", "ADDRESS", "INCOME",
                "SOURCE_OF_FUNDS"
            ]
        else:
            document_types = [
                "INCORPORATION", "ADDRESS", "OWNERSHIP",
                "DIRECTORS", "SOURCE_OF_FUNDS"
            ]

        document_type = random.choice(document_types)

        issue_date = TODAY - timedelta(
            days=random.randint(30, 1500)
        )

        expiry_date = TODAY + timedelta(
            days=random.randint(30, 1000)
        )

        status = random.choices(
            ["VERIFIED", "PENDING", "REJECTED"],
            weights=[70, 20, 10]
        )[0]

        holder_name = customer.full_name

        # Edge case 1: Expired but verified document.
        if (
            customer.customer_id == "CUS-000001"
            and doc_number == 1
        ):
            document_type = "IDENTITY"
            issue_date = TODAY - timedelta(days=365)
            expiry_date = TODAY - timedelta(days=30)
            status = "VERIFIED"

            duplicate_template = (
                document_type,
                issue_date,
                expiry_date,
                status,
                holder_name
            )

        # Edge case 2: Duplicate evidence across customers.
        elif (
            customer.customer_id == "CUS-000002"
            and doc_number == 1
            and duplicate_template is not None
        ):
            (
                document_type,
                issue_date,
                expiry_date,
                status,
                holder_name
            ) = duplicate_template

        elif customer.customer_id == "CUS-000004" and doc_number == 1:
            holder_name = "Incorrect Test Name"

        document_id = (
            f"DOC-{customer.customer_id}-{doc_number:03d}"
        )

        session.add(
            Document(
                document_id=document_id,
                customer_id=customer.customer_id,
                document_type=document_type,
                issue_date=issue_date,
                expiry_date=expiry_date,
                document_status=status,
                holder_name=holder_name
            )
        )

        verification_status = {
            "VERIFIED": "APPROVED",
            "PENDING": "PENDING",
            "REJECTED": "REJECTED"
        }[status]

        session.add(
            Verification(
                verification_id=(
                    f"VER-{verification_counter:06d}"
                ),
                document_id=document_id,
                verification_status=verification_status,
                verified_at=(
                    datetime(2026, 11, 10)
                    if status != "PENDING" else None
                ),
                reviewer=(
                    "SYSTEM_REVIEWER"
                    if status != "PENDING" else None
                )
            )
        )

        session.add(
            AuditEvent(
                event_id=f"AUD-DOC-{audit_counter:08d}",
                entity_type="DOCUMENT",
                entity_id=document_id,
                event_type="DOCUMENT_CREATED",
                new_value=status,
                reason="Synthetic document generation",
                actor="SYSTEM",
                created_at=datetime(2026, 11, 10)
            )
        )

        verification_counter += 1
        audit_counter += 1
        generated += 1

    session.commit()

    print("Documents generated:", generated)
    print("Verifications generated:", generated)


def generate_beneficial_owners(session):
    businesses = session.query(Customer).filter_by(
        customer_type_id="TYPE-002"
    ).order_by(Customer.customer_id).all()

    counter = 1

    for business in businesses:

        # Edge case: Business has no beneficial ownership records.
        if business.customer_id == "CUS-000016":
            continue

        # Edge case: Ownership exceeds 100%.
        first_percentage = (
            110.0
            if business.customer_id == "CUS-000008"
            else 60.0
        )

        session.add_all([
            BeneficialOwner(
                owner_id=f"OWN-{counter:06d}",
                customer_id=business.customer_id,
                owner_name=f"Owner A - {business.full_name}",
                ownership_percentage=first_percentage
            ),
            BeneficialOwner(
                owner_id=f"OWN-{counter + 1:06d}",
                customer_id=business.customer_id,
                owner_name=f"Owner B - {business.full_name}",
                ownership_percentage=40.0
            )
        ])

        counter += 2

    session.commit()
    print("Beneficial owners generated:", counter - 1)


def generate_review_cases(session, total_reviews):
    customers = session.query(Customer).order_by(
        Customer.customer_id
    ).all()

    statuses = ["OPEN", "IN_PROGRESS", "CLOSED"]

    for i in range(1, total_reviews + 1):
        customer = customers[
            (i - 1) % len(customers)
        ]

        status = random.choice(statuses)

        resolution = (
            "Review completed successfully"
            if status == "CLOSED" else None
        )

        due_date = TODAY + timedelta(
            days=random.randint(-30, 60)
        )

        # Edge case: Closed review without resolution.
        if i == 1:
            status = "CLOSED"
            resolution = None

        # Ensure an overdue open review exists.
        if i == 2:
            status = "OPEN"
            resolution = None
            due_date = TODAY - timedelta(days=5)

        session.add(
            ReviewCase(
                review_id=f"REV-{i:06d}",
                customer_id=customer.customer_id,
                review_date=date(2026, 10, 1),
                due_date=due_date,
                review_status=status,
                resolution=resolution
            )
        )

    session.commit()
    print("Review cases generated:", total_reviews)


def generate_alerts(session):
    documents = session.query(Document).all()
    counter = 1

    for document in documents:
        if (
            document.expiry_date is not None
            and document.expiry_date < TODAY
        ):
            session.add(
                Alert(
                    alert_id=f"ALT-{counter:06d}",
                    customer_id=document.customer_id,
                    alert_type="DOCUMENT_EXPIRED",
                    alert_message=(
                        f"Document {document.document_id} has expired."
                    ),
                    created_at=datetime(2026, 11, 10),
                    alert_status="OPEN"
                )
            )
            counter += 1

    reviews = session.query(ReviewCase).filter(
        ReviewCase.due_date < TODAY
    ).all()

    for review in reviews:
        if review.review_status != "CLOSED":
            session.add(
                Alert(
                    alert_id=f"ALT-{counter:06d}",
                    customer_id=review.customer_id,
                    alert_type="OVERDUE_REVIEW",
                    alert_message=(
                        f"Review {review.review_id} is overdue."
                    ),
                    created_at=datetime(2026, 11, 10),
                    alert_status="OPEN"
                )
            )
            counter += 1

    session.commit()
    print("Alerts generated:", counter - 1)


def generate_customer_audit_events(session):
    customers = session.query(Customer).all()
    counter = 1

    for customer in customers:
        session.add(
            AuditEvent(
                event_id=f"AUD-CUS-{counter:08d}",
                entity_type="CUSTOMER",
                entity_id=customer.customer_id,
                event_type="CUSTOMER_CREATED",
                new_value=customer.full_name,
                reason="Synthetic customer generation",
                actor="SYSTEM",
                created_at=datetime(2026, 1, 1)
            )
        )
        counter += 1

    session.commit()
    print("Customer audit events generated:", counter - 1)


def main():
    parser = argparse.ArgumentParser(
        description="KYC synthetic data generator"
    )

    parser.add_argument(
        "--scale",
        choices=["starter", "full"],
        default="starter"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=SEED
    )

    args = parser.parse_args()
    random.seed(args.seed)

    total_customers = (
        100 if args.scale == "starter" else 8000
    )

    total_documents = (
        250 if args.scale == "starter" else 20000
    )

    total_reviews = (
        30 if args.scale == "starter" else 3000
    )

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        print("\nStarting KYC data generation...")

        generate_master_data(session)
        generate_customers(session, total_customers)
        generate_documents(session, total_documents)
        generate_beneficial_owners(session)
        generate_review_cases(session, total_reviews)
        generate_alerts(session)
        generate_customer_audit_events(session)

        print("\nGeneration completed successfully!")
        print("Customers:", total_customers)
        print("Documents:", total_documents)
        print("Reviews:", total_reviews)
        print("Seed:", args.seed)
        print("Scale:", args.scale)

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()