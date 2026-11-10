
import csv
import json
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

ground_truth = [
    {
        "case_id": "GT-001",
        "scenario": "Expired document marked verified",
        "customer_id": "CUS-000001",
        "expected_issue": "Document is expired but marked VERIFIED",
        "severity": "HIGH"
    },
    {
        "case_id": "GT-002",
        "scenario": "Approved customer missing mandatory evidence",
        "customer_id": "CUS-000003",
        "expected_issue": "Approved customer has no supporting documents",
        "severity": "CRITICAL"
    },
    {
        "case_id": "GT-003",
        "scenario": "Ownership exceeds 100 percent",
        "customer_id": "CUS-000008",
        "expected_issue": "Total beneficial ownership exceeds 100%",
        "severity": "HIGH"
    },
    {
        "case_id": "GT-004",
        "scenario": "Closed review without resolution",
        "customer_id": "",
        "expected_issue": "Review is CLOSED but resolution is missing",
        "severity": "MEDIUM"
    },
    {
        "case_id": "GT-005",
        "scenario": "Potential duplicate document",
        "customer_id": "CUS-000001;CUS-000002",
        "expected_issue": "Matching document details exist across customers",
        "severity": "MEDIUM"
    },
    {
        "case_id": "GT-006",
        "scenario": "Overdue review",
        "customer_id": "",
        "expected_issue": "Open review has a due date before the generation date",
        "severity": "HIGH"
    },
    {
        "case_id": "GT-007",
        "scenario": "Document holder name mismatch",
        "customer_id": "CUS-000004",
        "expected_issue": "Document holder name does not match the customer's full name",
        "severity": "HIGH"
    },
    {
        "case_id": "GT-008",
        "scenario": "Business missing beneficial owners",
        "customer_id": "CUS-000016",
        "expected_issue": "Business customer has no beneficial ownership records",
        "severity": "HIGH"
    }
]

# Export JSON
json_path = DATA_DIR / "ground_truth.json"

with open(json_path, "w", encoding="utf-8") as file:
    json.dump(ground_truth, file, indent=4)

# Export CSV
csv_path = DATA_DIR / "ground_truth.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=ground_truth[0].keys()
    )
    writer.writeheader()
    writer.writerows(ground_truth)

print("Ground truth exports completed!")
print("Total scenarios:", len(ground_truth))
print("Created:", json_path)
print("Created:", csv_path)
