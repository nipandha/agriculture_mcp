from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_INPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "Custom_Crops_yield_Historical_Dataset.csv"
)
DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "districts.csv"
REQUIRED_COLUMNS = {"Dist Code", "Dist Name"}


def generate_district_csv(
    input_path: str | Path = DEFAULT_INPUT_PATH,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
) -> int:
    """Write unique district codes and names to a smaller CSV file."""
    input_path = Path(input_path)
    output_path = Path(output_path)

    with input_path.open("r", newline="", encoding="utf-8-sig") as input_file:
        reader = csv.DictReader(input_file)
        columns = set(reader.fieldnames or [])
        missing_columns = REQUIRED_COLUMNS - columns
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"input CSV is missing required column(s): {missing}")

        districts = {
            (row["Dist Code"].strip(), row["Dist Name"].strip())
            for row in reader
            if row["Dist Code"].strip() and row["Dist Name"].strip()
        }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=["Dist Code", "Dist Name"])
        writer.writeheader()
        writer.writerows(
            {"Dist Code": code, "Dist Name": name}
            for code, name in sorted(districts, key=lambda item: (int(item[0]), item[1]))
        )

    return len(districts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a CSV containing unique district codes and names."
    )
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT_PATH)
    arguments = parser.parse_args()

    count = generate_district_csv(arguments.input, arguments.output)
    print(f"Wrote {count} unique districts to {arguments.output}")
