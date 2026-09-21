from pathlib import Path
import argparse

from database.create_schema import DATABASE_PATH


def delete_database(database_path: str | Path = DATABASE_PATH) -> bool:
    """Delete a SQLite database and its temporary sidecar files."""
    database_path = Path(database_path)
    deleted = False

    for path in (
        database_path,
        Path(f"{database_path}-wal"),
        Path(f"{database_path}-shm"),
    ):
        if path.exists():
            path.unlink()
            deleted = True

    return deleted


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete the agriculture SQLite database.")
    parser.add_argument(
        "--database",
        type=Path,
        default=DATABASE_PATH,
        help=f"database path to delete (default: {DATABASE_PATH})",
    )
    arguments = parser.parse_args()

    if delete_database(arguments.database):
        print(f"Deleted database: {arguments.database}")
    else:
        print(f"Database not found: {arguments.database}")