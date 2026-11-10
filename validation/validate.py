
from datetime import date

from app.database import SessionLocal
from app.models import (
    Customer,
    Document,
    ReviewCase,
    BeneficialOwner,
    KYCRequirement
)

TODAY = date(2026, 11, 10)


def validate_database():
    session = SessionLocal()

    try:
        print("\nKYC DATABASE VALIDATION")
        print("=" * 35)

        customers = session.query(Customer).all()
        documents = session.query(Document).all()
        reviews = session.query(ReviewCase).all()
        owners = session.query(BeneficialOwner).all()

        # Check 1: Customer count
        print("\n1. Customer count:", len(customers))

        # Check 2: Documents linked to customers
        customer_ids = {c.customer_id for c in customers}

        invalid_documents = [
            d for d in documents
            if d.customer_id not in customer_ids
        ]

        print("2. Documents without valid customers:",
              len(invalid_documents))

        # Check 3: Expired documents marked verified
        expired_verified = [
            d for d in documents
            if d.expiry_date is not None
            and d.expiry_date < TODAY
            and d.document_status == "VERIFIED"
        ]

        print("3. Expired verified documents:",
              len(expired_verified))

        # Check 4: Approved customers missing mandatory evidence
        requirements = session.query(KYCRequirement).filter_by(
            is_mandatory=True
        ).all()

        approved_customers = [
            c for c in customers
            if c.onboarding_status == "APPROVED"
        ]

        missing_evidence = []

        for customer in approved_customers:
            customer_documents = [
                d for d in documents
                if d.customer_id == customer.customer_id
                and d.document_status == "VERIFIED"
            ]

            required_types = {
                r.document_type
                for r in requirements
                if r.customer_type_id == customer.customer_type_id
            }

            available_types = {
                d.document_type for d in customer_documents
            }

            if required_types - available_types:
                missing_evidence.append(customer.customer_id)

        print("4. Approved customers missing mandatory evidence:",
              len(missing_evidence))

        # Check 5: Ownership above 100%
        ownership_totals = {}

        for owner in owners:
            ownership_totals[owner.customer_id] = (
                ownership_totals.get(owner.customer_id, 0)
                + owner.ownership_percentage
            )

        excessive_ownership = {
            customer_id: total
            for customer_id, total in ownership_totals.items()
            if total > 100
        }

        print("5. Businesses with ownership above 100%:",
              len(excessive_ownership))

        # Check 6: Closed reviews without resolution
        unresolved_closed = [
            r for r in reviews
            if r.review_status == "CLOSED"
            and not r.resolution
        ]

        print("6. Closed reviews without resolution:",
              len(unresolved_closed))

        # Check 7: Duplicate documents
        duplicate_groups = {}

        for d in documents:
            key = (
                d.document_type,
                d.issue_date,
                d.expiry_date,
                d.holder_name
            )

            duplicate_groups.setdefault(key, []).append(d)

        duplicates = [
            group for group in duplicate_groups.values()
            if len(group) > 1
        ]

        print("7. Potential duplicate document groups:",
              len(duplicates))

        # Check 8: Overdue reviews
        overdue_reviews = [
            r for r in reviews
            if r.due_date < TODAY
            and r.review_status != "CLOSED"
        ]

        print("8. Overdue open reviews:",
              len(overdue_reviews))

        # Check 9: Document holder name mismatch
        customer_names = {
            c.customer_id: c.full_name
            for c in customers
        }

        name_mismatches = [
            d for d in documents
            if d.customer_id in customer_names
            and d.holder_name != customer_names[d.customer_id]
        ]

        print("9. Document holder name mismatches:",
              len(name_mismatches))

        # Check 10: Businesses missing beneficial owners
        business_customers = [
            c for c in customers
            if c.customer_type_id == "TYPE-002"
        ]

        businesses_with_owners = {
            owner.customer_id for owner in owners
        }

        missing_owners = [
            c for c in business_customers
            if c.customer_id not in businesses_with_owners
        ]

        print("10. Businesses missing beneficial owners:",
              len(missing_owners))

        print("\nValidation completed!")

    finally:
        session.close()


if __name__ == "__main__":
    validate_database()
