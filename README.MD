# KYC Evidence & Review Management System

## 1. Project Overview

The KYC Evidence & Review Management System is a Python-based synthetic data generation and validation project designed to support Know Your Customer (KYC) onboarding, evidence tracking, risk assessment, and periodic review workflows.

It generates realistic synthetic KYC records, identifies data-quality issues, validates business rules, and exports datasets in CSV, JSON, and SQL formats.

## 2. Key Features

- Synthetic customer and business data generation.
- KYC requirements based on customer type.
- Document and verification tracking.
- Customer risk ratings.
- Beneficial ownership records.
- Periodic KYC review cases.
- Alerts for expired documents and overdue reviews.
- Audit event tracking.
- Ground-truth scenarios for known data-quality issues.
- Automated validation and testing.
- SHA-256 checksums for reproducibility.

## 3. Technology Stack

- Python 3.11
- SQLite
- SQLAlchemy
- Pandas
- NumPy
- Pytest

## 4. Dataset Details

The full dataset contains:

| Entity | Records |
|---|---:|
| Customers | 8,000 |
| Customer Types | 2 |
| KYC Requirements | 9 |
| Documents | 20,000 |
| Verifications | 20,000 |
| Risk Ratings | 8,000 |
| Beneficial Owners | 2,000 |
| Review Cases | 3,000 |
| Alerts | 665 |
| Audit Events | 28,000 |

## 5. Project Structure

- `app/` – Database configuration and SQLAlchemy models.
- `generator/` – Synthetic data generation, exports, ground truth, and checksum scripts.
- `data/` – Generated CSV, JSON, SQL, ground-truth, and checksum files.
- `validation/` – Database validation rules.
- `tests/` – Automated business-rule tests.
- `schema/` – Data dictionary and schema documentation.

## 6. Setup Instructions

Clone the repository and navigate into the project directory.

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 7. Generate Synthetic Data

Generate the starter dataset:

```bash
python -m generator.generate_data --scale starter
```

Generate the full dataset:

```bash
python -m generator.generate_data --scale full
```

Use a fixed seed for reproducibility:

```bash
python -m generator.generate_data --scale full --seed 20261022
```

## 8. Export Data

Export all database tables to CSV and JSON, and export the SQLite database as SQL:

```bash
python -m generator.export_data
```

Generate ground-truth files:

```bash
python -m generator.generate_ground_truth
```

Generate SHA-256 checksums:

```bash
python -m generator.checksum
```

## 9. Run Validation

Execute database validation:

```bash
python -m validation.validate
```

The validation checks include:

1. Customer record count.
2. Invalid customer references in documents.
3. Expired documents marked as verified.
4. Approved customers missing mandatory evidence.
5. Beneficial ownership exceeding 100%.
6. Closed review cases without resolution.
7. Potential duplicate documents.
8. Overdue open review cases.

## 10. Run Automated Tests

Run the test suite:

```bash
python -m pytest -q
```

## 11. Ground Truth Scenarios

The ground-truth dataset contains eight intentional data-quality scenarios:

1. Expired document marked as verified.
2. Approved customer missing mandatory evidence.
3. Beneficial ownership exceeding 100%.
4. Closed review without resolution.
5. Potential duplicate documents.
6. Overdue review case.
7. Document holder name mismatch.
8. Business missing beneficial owners.

These scenarios help verify that the validation logic identifies known data-quality issues.

The ground-truth files are available in `data/ground_truth.csv` and `data/ground_truth.json`.

## 12. Reproducibility

The project uses a fixed random seed (`20261022`) and fixed timestamps to support deterministic data generation.

SHA-256 checksums are generated for exported files. Two full generation runs using the same seed produced identical checksums.

## 13. Database

The project uses SQLite with SQLAlchemy ORM models.

Database file: `kyc_management.db`

The database contains customer, document, verification, risk, review, ownership, alert, and audit records.

## 14. Advance Document Expiry Alerts

The API supports configurable advance warnings for documents approaching their expiry date.

**Endpoint:** `POST /alerts/check-expiring-documents`

**Parameter:**
- `warning_days`: Number of days before expiry to check. Defaults to 30 and accepts values from 1 to 365.

**How it works:**
- Finds documents expiring within the configured warning period.
- Creates `DOCUMENT_EXPIRING_SOON` alerts.
- Assigns unique alert IDs.
- Prevents duplicate alerts when the same check is run again.

**Example:** Set `warning_days=30` to identify documents expiring within the next 30 days.

The endpoint was tested with 53 matching documents. It created 53 alerts on the first run and 0 duplicate alerts on the second run.

## 15. Disclaimer

All generated records are synthetic and intended only for development, testing, and demonstration purposes. No real customer or personally identifiable information is used.