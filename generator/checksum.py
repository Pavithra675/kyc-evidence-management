
import hashlib
import json
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "checksums.json"


def calculate_checksum(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def main():
    checksums = {}

    for file_path in sorted(DATA_DIR.iterdir()):
        if file_path.is_file() and file_path.name != OUTPUT_FILE.name:
            checksums[file_path.name] = calculate_checksum(file_path)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(checksums, file, indent=4)

    print("SHA-256 checksums generated!")
    print("Files checked:", len(checksums))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
