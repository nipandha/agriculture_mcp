from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path

from database.create_schema import DATABASE_PATH, create_schema


DEFAULT_INPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "Custom_Crops_yield_Historical_Dataset.csv"
)

CSV_COLUMNS = (
    "Dist Code",
    "Year",
    "State Code",
    "State Name",
    "Dist Name",
    "Crop",
    "Area_ha",
    "Yield_kg_per_ha",
    "N_req_kg_per_ha",
    "P_req_kg_per_ha",
    "K_req_kg_per_ha",
    "Total_N_kg",
    "Total_P_kg",
    "Total_K_kg",
    "Temperature_C",
    "Humidity_%",
    "pH",
    "Rainfall_mm",
    "Wind_Speed_m_s",
    "Solar_Radiation_MJ_m2_day",
)

INTEGER_COLUMNS = {"Dist Code", "Year", "State Code"}
TEXT_COLUMNS = {"State Name", "Dist Name", "Crop"}
DATABASE_COLUMNS = (
    "dist_code",
    "year",
    "state_code",
    "state_name",
    "dist_name",
    "crop",
    "area_ha",
    "yield_kg_per_ha",
    "n_req_kg_per_ha",
    "p_req_kg_per_ha",
    "k_req_kg_per_ha",
    "total_n_kg",
    "total_p_kg",
    "total_k_kg",
    "temperature_c",
    "humidity_percent",
    "ph",
    "rainfall_mm",
    "wind_speed_m_s",
    "solar_radiation_mj_m2_day",
)
INSERT_SQL = f"""
INSERT OR REPLACE INTO crop_yields ({", ".join(DATABASE_COLUMNS)})
VALUES ({", ".join("?" for _ in DATABASE_COLUMNS)})
"""


def _convert_row(row: dict[str, str | None], row_number: int) -> tuple[object, ...]:
    values: list[object] = []
    for column in CSV_COLUMNS:
        value = (row.get(column) or "").strip()
        if not value:
            raise ValueError(f"row {row_number}: missing value for {column!r}")
        try:
            if column in INTEGER_COLUMNS:
                values.append(int(value))
            elif column in TEXT_COLUMNS:
                values.append(value)
            else:
                values.append(float(value))
        except ValueError as error:
            raise ValueError(
                f"row {row_number}: invalid value {value!r} for {column!r}"
            ) from error
    return tuple(values)


def import_csv_to_database(
    input_path: str | Path = DEFAULT_INPUT_PATH,
    database_path: str | Path = DATABASE_PATH,
) -> int:
    """Import all CSV rows into the crop_yields SQLite table."""
    input_path = Path(input_path)
    database_path = Path(database_path)
    create_schema(database_path)

    with input_path.open("r", newline="", encoding="utf-8-sig") as input_file:
        reader = csv.DictReader(input_file)
        missing_columns = set(CSV_COLUMNS) - set(reader.fieldnames or [])
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"input CSV is missing required column(s): {missing}")

        connection = sqlite3.connect(database_path)
        try:
            rows_imported = 0
            with connection:
                for row_number, row in enumerate(reader, start=2):
                    connection.execute(INSERT_SQL, _convert_row(row, row_number))
                    rows_imported += 1
        finally:
            connection.close()

    return rows_imported


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Import the crop-yield CSV into the SQLite database."
    )
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--database", type=Path, default=DATABASE_PATH)
    arguments = parser.parse_args()

    count = import_csv_to_database(arguments.input, arguments.database)
    print(f"Imported {count} rows into {arguments.database}")
