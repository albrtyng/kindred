from pathlib import Path

from dotenv import load_dotenv


def pytest_configure() -> None:
    """Load the local test profile, falling back to the committed template."""
    backend_directory = Path(__file__).parent.parent
    environment_file = backend_directory / ".env.test"
    if not environment_file.exists():
        environment_file = backend_directory / ".env.test.example"

    load_dotenv(environment_file, override=True)
