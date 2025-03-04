import tomlkit
from pathlib import Path


def get_toml_doc(path: Path) -> tomlkit.TOMLDocument:
    """Reads a TOML file and returns its parsed document."""
    with path.open(mode="r") as f:
        return tomlkit.loads(f.read())


def format_list_multiline(items: list) -> tomlkit.items.Array:
    """Formats list items to appear on multiple lines in TOML output."""
    arr = tomlkit.array()
    for item in items:
        arr.append(item)
    arr.multiline(True)
    return arr


def write_to_pyproject_toml(metadata: dict, path: Path):
    """Writes the converted metadata to a new TOML file with proper formatting."""
    with path.open(mode="w") as f:
        tomlkit.dump(metadata, f)
