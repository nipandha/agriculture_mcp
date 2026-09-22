# Agriculture MCP Server

This project provides a FastMCP server for querying agriculture and crop-yield data stored in a SQLite database. It exposes structured data access for district, crop, and year-based agricultural analysis.

## Overview

The application reads crop-yield data from the CSV file in the `data/` directory, imports it into a SQLite database, and exposes it through MCP tools and resources.

This allows client applications to:
- query specific agricultural fields
- filter by district, crop, and year range
- inspect valid fields, districts, crops, and years
- use the data in a simple, structured way through MCP

## Project Structure

- `server.py` — MCP server entry point
- `requirements.txt` — Python dependencies
- `data/` — source CSV dataset
- `database/` — database schema, import, and read helpers
  - `create_schema.py` — creates the SQLite schema
  - `import_csv_to_database.py` — imports the CSV dataset into SQLite
  - `read_database.py` — data query helpers
  - `print_database.py` — useful debugging utility for checking database contents
  - `delete_database.py` — removes the SQLite database

## Data Source

The dataset used by the project is:

- `data/Custom_Crops_yield_Historical_Dataset.csv`

It contains agricultural metrics such as:
- district code and name
- state name and code
- crop name
- year
- area and yield
- nutrient requirement values
- temperature, humidity, pH, rainfall, wind speed, and solar radiation

## Requirements

- Python 3.10+
- `pip` package installer

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Import the CSV dataset into SQLite:

```bash
python database/import_csv_to_database.py
```

4. Start the MCP server:

```bash
python server.py
```

## Available MCP Tools

### `query_database`

Query agricultural data with optional filters.

Parameters:
- `fields`: list of fields to return
- `district`: optional district name
- `crop`: optional crop name
- `year_start`: optional starting year
- `year_end`: optional ending year

Example:

```python
query_database(
    fields=["year", "dist_name", "crop", "yield_kg_per_ha"],
    district="Agra",
    crop="Wheat",
    year_start=2018,
    year_end=2023,
)
```

To get information for only one year, set both `year_start` and `year_end` to the same value:

```python
query_database(
    fields=["year", "dist_name", "crop", "yield_kg_per_ha"],
    district="Agra",
    crop="Wheat",
    year_start=2023,
    year_end=2023,
)
```

## Available MCP Resources

The server exposes these resources:

- `fields://allowed` — returns all valid database fields
- `catalog://{name}` — returns catalog data for crops, districts, and years
- `districts://all` — returns all district names
- `years://all` — returns all available years
- `crops://all` — returns all crop names

## Database Schema

The SQLite table is named `crop_yields` and includes fields such as:

- `dist_code`
- `year`
- `state_code`
- `state_name`
- `dist_name`
- `crop`
- `area_ha`
- `yield_kg_per_ha`
- `n_req_kg_per_ha`
- `p_req_kg_per_ha`
- `k_req_kg_per_ha`
- `total_n_kg`
- `total_p_kg`
- `total_k_kg`
- `temperature_c`
- `humidity_percent`
- `ph`
- `rainfall_mm`
- `wind_speed_m_s`
- `solar_radiation_mj_m2_day`

## Notes

- The database file is created in `database/agriculture.db`.
- If needed, you can reset the database using the scripts in the `database/` folder.
- The project is built around `FastMCP` and is designed to expose agricultural data to MCP-compatible clients.

## License

This project does not currently specify a license. If you plan to share or distribute it, add a license file and documentation accordingly.
