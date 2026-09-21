from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from database.create_schema import DATABASE_PATH


PAGE_SIZE = 50


def print_database(database_path: str | Path = DATABASE_PATH) -> None:
    """Print the database 50 rows at a time until the user quits."""
    database_path = Path(database_path)
    if not database_path.exists():
        raise FileNotFoundError(f"database not found: {database_path}")

    connection = sqlite3.connect(database_path)
    try:
        cursor = connection.execute(
            "SELECT * FROM crop_yields ORDER BY dist_code, year, crop"
        )
        headers = [column[0] for column in cursor.description or ()]
        page_number = 1

        while True:
            rows = cursor.fetchmany(PAGE_SIZE)
            if not rows:
                if page_number == 1:
                    print("The database is empty.")
                else:
                    print("End of database.")
                break

            print(f"\n--- Page {page_number} ({len(rows)} rows) ---")
            print("\t".join(headers))
            for row in rows:
                print("\t".join(str(value) for value in row))

            if len(rows) < PAGE_SIZE:
                print("\nEnd of database.")
                break

            response = input("\nPress Enter for the next 50 rows, or enter q to quit: ")
            if response.strip().lower() == "q":
                break
            page_number += 1
    finally:
        connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print the agriculture database 50 rows at a time."
    )
    parser.add_argument("--database", type=Path, default=DATABASE_PATH)
    arguments = parser.parse_args()
    print_database(arguments.database)
