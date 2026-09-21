from pathlib import Path
import sqlite3


DATABASE_PATH = Path(__file__).resolve().parent / "agriculture.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS crop_yields (
    dist_code INTEGER NOT NULL,
    year INTEGER NOT NULL,
    state_code INTEGER NOT NULL,
    state_name TEXT NOT NULL,
    dist_name TEXT NOT NULL,
    crop TEXT NOT NULL,
    area_ha REAL NOT NULL,
    yield_kg_per_ha REAL NOT NULL,
    n_req_kg_per_ha REAL NOT NULL,
    p_req_kg_per_ha REAL NOT NULL,
    k_req_kg_per_ha REAL NOT NULL,
    total_n_kg REAL NOT NULL,
    total_p_kg REAL NOT NULL,
    total_k_kg REAL NOT NULL,
    temperature_c REAL NOT NULL,
    humidity_percent REAL NOT NULL,
    ph REAL NOT NULL,
    rainfall_mm REAL NOT NULL,
    wind_speed_m_s REAL NOT NULL,
    solar_radiation_mj_m2_day REAL NOT NULL,
    PRIMARY KEY (dist_code, year, crop)
);

CREATE INDEX IF NOT EXISTS idx_crop_yields_state_year
    ON crop_yields (state_code, year);

CREATE INDEX IF NOT EXISTS idx_crop_yields_crop_year
    ON crop_yields (crop, year);
"""



def create_schema(database_path: str | Path = DATABASE_PATH) -> None:
    """Create the agriculture database tables and indexes."""
    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    try:
        connection.executescript(SCHEMA_SQL)
    finally:
        connection.close()





if __name__ == "__main__":
    create_schema()
    print(f"Created schema in {DATABASE_PATH}")