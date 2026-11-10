
import csv
import json
import sqlite3
from pathlib import Path

from app.database import engine, Base
from app import models

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def export_tables():
    print("Starting data exports...")

    for table in Base.metadata.sorted_tables:
        table_name = table.name

        with engine.connect() as connection:
            rows = connection.execute(
                table.select()
            ).mappings().all()

        records = [dict(row) for row in rows]

        # Export CSV
        csv_path = DATA_DIR / f"{table_name}.csv"

        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[column.name for column in table.columns]
            )
            writer.writeheader()
            writer.writerows(records)

        # Export JSON
        json_path = DATA_DIR / f"{table_name}.json"

        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, default=str)

        print(f"Exported: {table_name} ({len(records)} records)")


def export_sql():
    database_path = Path("kyc_management.db")
    sql_path = DATA_DIR / "kyc_management.sql"

    connection = sqlite3.connect(database_path)

    try:
        with open(sql_path, "w", encoding="utf-8") as file:
            for line in connection.iterdump():
                file.write(line + "\n")
    finally:
        connection.close()

    print("SQL export completed!")


def main():
    export_tables()
    export_sql()
    print("\nAll exports completed successfully!")


if __name__ == "__main__":
    main()
