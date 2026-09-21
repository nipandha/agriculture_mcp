import sqlite3

from database.create_schema import DATABASE_PATH
ALLOWED_FIELDS = frozenset(
    {
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
    }
)

DISCRETE_ALLOWED_FIELDS = frozenset(
    {
        "dist_code",
        "year",
        "state_code",
        "state_name",
        "dist_name",
        "crop",
    }
)

def get_db_allowed_fields() -> list[str]:
    """Return the fields that can be requested from get_data."""
    return sorted(ALLOWED_FIELDS)


def get_discrete_allowed_fields() -> list[str]:
    """Return allowed fields suitable for unique-value lookups."""
    return sorted(DISCRETE_ALLOWED_FIELDS)


def get_unique_values(field: str) -> list[object]:
    """Return the distinct values for one discrete allowed field."""
    if field not in DISCRETE_ALLOWED_FIELDS:
        raise ValueError(f"field is not discrete or is unknown: {field}")

    connection = sqlite3.connect(DATABASE_PATH)
    try:
        rows = connection.execute(
            f"SELECT DISTINCT {field} FROM crop_yields ORDER BY {field}"
        ).fetchall()
        return [row[0] for row in rows]
    finally:
        connection.close()


def get_data(
    fields: list[str],
    district: str | None = None,
    crop: str | None = None,
    year_start: int | None = None,
    year_end: int | None = None,
) -> list[dict[str, object]]:
    """Return selected crop-yield fields matching the optional filters."""
    if not fields:
        raise ValueError("fields must contain at least one column name")

    unknown_fields = set(fields) - ALLOWED_FIELDS
    if unknown_fields:
        names = ", ".join(sorted(unknown_fields))
        raise ValueError(f"unknown field(s): {names}")

    if year_start is not None and year_end is not None and year_start > year_end:
        raise ValueError("year_start must be less than or equal to year_end")

    query = [f"SELECT {', '.join(fields)} FROM crop_yields"]
    parameters: list[object] = []
    conditions: list[str] = []

    if district is not None:
        conditions.append("dist_name = ?")
        parameters.append(district)
    if crop is not None:
        conditions.append("crop = ?")
        parameters.append(crop)
    if year_start is not None:
        conditions.append("year >= ?")
        parameters.append(year_start)
    if year_end is not None:
        conditions.append("year <= ?")
        parameters.append(year_end)

    if conditions:
        query.append("WHERE " + " AND ".join(conditions))
    query.append("ORDER BY year, dist_name, crop")

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(" ".join(query), parameters).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()