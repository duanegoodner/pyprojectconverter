import argparse
from pathlib import Path

import toml_utils as tu
import tomlkit

# def get_toml_doc(path: Path) -> tomlkit.TOMLDocument:
#     """Reads a TOML file and returns its parsed document."""
#     with path.open(mode="r") as f:
#         return tomlkit.loads(f.read())


def convert_version(pip_version: str) -> str:
    """
    Converts pip-style version constraints to Poetry-compatible versions:
    - ">=X.Y.Z,<(X+1).0.0" → "^X.Y.Z"
    - "==X.Y.Z" → "X.Y.Z" (pinned version)
    - No constraint → "*"
    """
    if not pip_version or pip_version == "*":
        return "*"

    if "==" in pip_version:
        return pip_version.replace("==", "")  # Exact match, no caret needed

    if ">=" in pip_version and "<" in pip_version:
        min_version = pip_version.split(",")[0].replace(">=", "")
        return f"^{min_version}"  # Convert to caret-style

    return pip_version


def get_dependencies(pip_metadata: dict) -> dict:
    """Extracts dependencies and converts them to Poetry format."""
    dependencies = {}
    for dep in pip_metadata.get("dependencies", []):
        name, *version = dep.split(">=") if ">=" in dep else dep.split("==")
        dependencies[name.strip()] = convert_version(">=".join(version).strip()) if version else "*"
    return dependencies


def get_dev_dependencies(pip_metadata: dict) -> dict:
    """Extracts dev dependencies and converts them to Poetry format."""
    optional_deps = pip_metadata.get("optional-dependencies", {})
    dev_dependencies = {}
    if "dev" in optional_deps:
        for dev_dep in optional_deps["dev"]:
            name, *version = dev_dep.split(">=") if ">=" in dev_dep else dev_dep.split("==")
            dev_dependencies[name.strip()] = convert_version(">=".join(version).strip()) if version else "*"
    return dev_dependencies


def get_packages(pip_metadata: dict) -> list:
    """Extracts package discovery settings from setuptools and converts them to Poetry format."""
    if "tool" in pip_metadata and "setuptools" in pip_metadata["tool"]:
        setuptools_data = pip_metadata["tool"]["setuptools"]
        if "packages" in setuptools_data and "find" in setuptools_data["packages"]:
            return [{"include": "docktuna", "from": setuptools_data["packages"]["find"]["where"][0]}]
    return []


# def format_list_multiline(items: list) -> tomlkit.items.Array:
#     """Formats list items to appear on multiple lines in TOML output."""
#     arr = tomlkit.array()
#     for item in items:
#         arr.append(item)
#     arr.multiline(True)
#     return arr


def create_poetry_metadata(pip_metadata: dict, original_toml: tomlkit.TOMLDocument) -> dict:
    """Creates a Poetry-compatible project metadata structure while retaining all tool settings."""
    dependencies = get_dependencies(pip_metadata)
    dev_dependencies = get_dev_dependencies(pip_metadata)
    packages = get_packages(original_toml)

    poetry_metadata = tomlkit.document()
    poetry_metadata["tool"] = {}
    poetry_metadata["tool"]["poetry"] = {
        "name": pip_metadata["name"],
        "version": pip_metadata["version"],
        "description": pip_metadata["description"],
        "authors": pip_metadata["authors"],
        "license": pip_metadata.get("license", ""),
        "dependencies": {"python": "^3.11", **dependencies},
    }

    if dev_dependencies:
        poetry_metadata["tool"]["poetry"]["group"] = {
            "dev": {"dependencies": dev_dependencies}
        }

    if packages:
        poetry_metadata["tool"]["poetry"]["packages"] = packages

    poetry_metadata["build-system"] = {
        "requires": tu.format_list_multiline(["poetry-core"]),
        "build-backend": "poetry.core.masonry.api",
    }

    # Preserve all tool configurations except `tool.setuptools`
    for tool_key in original_toml.get("tool", {}):
        if tool_key != "setuptools":
            poetry_metadata["tool"][tool_key] = original_toml["tool"][tool_key]

    return poetry_metadata


# def write_to_pyproject_toml(poetry_metadata: dict, path: Path):
#     """Writes the converted metadata to a new TOML file with proper formatting."""
#     with path.open(mode="w") as f:
#         tomlkit.dump(poetry_metadata, f)


def main():
    """Converts a pip-based pyproject.toml back to a Poetry-compatible version."""
    parser = argparse.ArgumentParser(description="Convert pip pyproject.toml to Poetry-compatible format.")
    parser.add_argument("-i", "--input", type=Path, required=True, help="Path to the pip pyproject.toml file.")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Path to save the converted Poetry-compatible pyproject.toml file.")
    args = parser.parse_args()

    toml_doc = tu.get_toml_doc(path=args.input)
    pip_metadata = toml_doc["project"]
    poetry_metadata = create_poetry_metadata(pip_metadata=pip_metadata, original_toml=toml_doc)
    tu.write_to_pyproject_toml(metadata=poetry_metadata, path=args.output)

    print(f"✅ Successfully converted {args.input} to {args.output}!")


if __name__ == "__main__":
    main()
