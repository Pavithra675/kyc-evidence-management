
from sqlalchemy import (
    Column, String, Integer, Float, Boolean,
    Date, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


# 1. Customer Type
class CustomerType(Base):
    __tablename__ = "customer_types"

    customer_type_id = Column(String, primary_key=True)
    type_name = Column(String, unique=True, nullable=False)

    customers = relationship("Customer", back_populates="customer_type")


# 2. Customer
# 2. Customer
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)
    customer_type_id = Column(
        String,
        ForeignKey("customer_types.customer_type_id"),
        nullable=False
    )
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    onboarding_status = Column(
        String, nullable=False, default="PENDING"
    )
    created_at = Column(DateTime, default=lambda: datetime(2026, 11, 10, 12, 0, 0))

    customer_type = relationship(
        "CustomerType", back_populates="customers"
    )
    documents = relationship("Document", back_populates="customer")
    risk_rating = relationship(
        "RiskRating", back_populates="customer", uselist=False
    )
    reviews = relationship("ReviewCase", back_populates="customer")
    beneficial_owners = relationship(
        "BeneficialOwner", back_populates="customer"
    )

# 3. KYC Requirement
class KYCRequirement(Base):
    __tablename__ = "kyc_requirements"

    requirement_id = Column(String, primary_key=True)
    customer_type_id = Column(
        String, ForeignKey("customer_types.customer_type_id"),
        nullable=False
    )
    document_type = Column(String, nullable=False)
    risk_level = Column(String, nullable=False)
    is_mandatory = Column(Boolean, default=True)


# 4. Document
class Document(Base):
    __tablename__ = "documents"

    document_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"), nullable=False)
    document_type = Column(String, nullable=False)
    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    document_status = Column(String, nullable=False)
    holder_name = Column(String, nullable=False)

    customer = relationship("Customer", back_populates="documents")
    verifications = relationship("Verification", back_populates="document")


# 5. Verification
class Verification(Base):
    __tablename__ = "verifications"

    verification_id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey("documents.document_id"), nullable=False)
    verification_status = Column(String, nullable=False)
    verified_at = Column(DateTime, nullable=True)
    reviewer = Column(String, nullable=True)

    document = relationship("Document", back_populates="verifications")


# 6. Risk Rating
class RiskRating(Base):
    __tablename__ = "risk_ratings"

    risk_id = Column(String, primary_key=True)
    customer_id = Column(
        String, ForeignKey("customers.customer_id"),
        unique=True, nullable=False
    )
    risk_level = Column(String, nullable=False)
    risk_score = Column(Float, nullable=False)
    assessed_at = Column(DateTime, default=lambda: datetime(2026, 11, 10, 12, 0, 0))

    customer = relationship("Customer", back_populates="risk_rating")


# 7. Review Case
class ReviewCase(Base):
    __tablename__ = "review_cases"

    review_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"), nullable=False)
    review_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    review_status = Column(String, nullable=False)
    resolution = Column(Text, nullable=True)

    customer = relationship("Customer", back_populates="reviews")


# 8. Beneficial Owner
class BeneficialOwner(Base):
    __tablename__ = "beneficial_owners"

    owner_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"), nullable=False)
    owner_name = Column(String, nullable=False)
    ownership_percentage = Column(Float, nullable=False)

    customer = relationship("Customer", back_populates="beneficial_owners")


# 9. Alert
class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"), nullable=False)
    alert_type = Column(String, nullable=False)
    alert_message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime(2026, 11, 10, 12, 0, 0))
    alert_status = Column(String, default="OPEN")


# 10. Audit Event
class AuditEvent(Base):
    __tablename__ = "audit_events"

    event_id = Column(String, primary_key=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)
    actor = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime(2026, 11, 10, 12, 0, 0))
