import argparse
import json
from pathlib import Path

from kindred_api.main import app


def generate_openapi(output: Path) -> None:
    """Write FastAPI's OpenAPI document in a stable JSON representation."""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f"{json.dumps(app.openapi(), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the Kindred OpenAPI document.")
    parser.add_argument("--output", type=Path, default=Path("openapi.json"))
    arguments = parser.parse_args()
    generate_openapi(arguments.output)


if __name__ == "__main__":
    main()
