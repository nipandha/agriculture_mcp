from mcp.server import MCPServer
import json

from database.read_database import get_data, get_unique_values, get_db_allowed_fields

mcp = MCPServer("Agriculture")


@mcp.tool()
def query_database(fields: list[str],
    district: str | None = None,
    crop: str | None = None,
    year_start: int | None = None,
    year_end: int | None = None) -> list[dict[str, object]]:
    """Query the agriculture database."""
    return get_data(
        fields=fields,
        district=district,
        crop=crop,
        year_start=year_start,
        year_end=year_end
    )


@mcp.resource()
def get_allowed_fields() -> str:
    """Return the list of allowed fields."""
    return json.dumps({"allowed_fields": get_db_allowed_fields()})

@mcp.resource()
def get_catalog(name: str) -> str:
    """Return the catalog of available data."""
    return json.dumps({
        "crops": get_unique_values("crop"),
        "districts": get_unique_values("dist_name"),
        "years": get_unique_values("year")
    })

@mcp.resource()
def get_all_districts(name: str) -> str:
    """Return the list of all districts."""
    all_districts = get_unique_values("dist_name")
    return json.dumps({"districts": all_districts})

@mcp.resource()
def get_all_years(name: str) -> str:
    """Return the list of all years."""
    all_years = get_unique_values("year")
    return json.dumps({"years": all_years})

@mcp.resource()
def get_all_crops(name: str) -> str:
    """Return the list of all crops."""
    all_crops = get_unique_values("crop")
    return json.dumps({"crops": all_crops})