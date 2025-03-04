import argparse
from pathlib import Path

import toml_utils as tu
import tomlkit


# def get_toml_doc(path: Path) -> tomlkit.TOMLDocument:
#     """Reads a TOML file and returns its parsed document."""
#     with path.open(mode="r") as f:
#         return tomlkit.loads(f.read())


def convert_version(poetry_version: str) -> str:
    """
    Converts Poetry-style versions to pip-compatible versions:
    - "^X.Y.Z" → ">=X.Y.Z,<(X+1).0.0"
    - "X.Y.Z"  → "==X.Y.Z" (pinned version)
    - "*"      → "" (no version constraint)
    """
    if poetry_version == "*":
        return ""
    if poetry_version.startswith("^"):
        version_parts = poetry_version[1:].split(".")
        major_version = int(version_parts[0]) + 1
        return f">={poetry_version[1:]},<{major_version}.0.0"
    if poetry_version.replace(".", "").isdigit():  # Pinned versions
        return f"=={poetry_version}"
    return poetry_version


def get_dependencies(poetry_metadata: dict) -> list:
    """Extracts dependencies while converting version constraints."""
    return [
        f"{pkg}{convert_version(ver)}"
        for pkg, ver in poetry_metadata["dependencies"].items()
        if pkg.lower() != "python"
    ]


def get_dev_dependencies(poetry_metadata: dict) -> list:
    """Extracts dev dependencies from Poetry group.dev.dependencies."""
    if "group" in poetry_metadata and "dev" in poetry_metadata["group"]:
        return [
            f"{pkg}{convert_version(ver)}"
            for pkg, ver in poetry_metadata["group"]["dev"]["dependencies"].items()
        ]
    return []


def get_packages(poetry_metadata: dict) -> dict:
    """Extracts package discovery settings for setuptools if using src layout."""
    if "packages" in poetry_metadata:
        return {"find": {"where": [entry["from"]] for entry in poetry_metadata["packages"]}}
    return {"find": {}}


# def format_list_multiline(items: list) -> tomlkit.items.Array:
#     """Formats list items to appear on multiple lines in TOML output."""
#     arr = tomlkit.array()
#     for item in items:
#         arr.append(item)
#     arr.multiline(True)
#     return arr


def create_pip_metadata(poetry_metadata: dict, original_toml: tomlkit.TOMLDocument) -> dict:
    """Creates a pip-compatible project metadata structure while retaining all tool settings."""
    dependencies = get_dependencies(poetry_metadata)
    dev_dependencies = get_dev_dependencies(poetry_metadata)
    packages = get_packages(poetry_metadata)

    pip_metadata = tomlkit.document()
    pip_metadata["project"] = {
        "name": poetry_metadata["name"],
        "version": poetry_metadata["version"],
        "description": poetry_metadata["description"],
        "authors": poetry_metadata["authors"],
        "license": poetry_metadata.get("license", ""),
        "dependencies": tu.format_list_multiline(dependencies),
    }

    if dev_dependencies:
        pip_metadata["project"]["optional-dependencies"] = {
            "dev": tu.format_list_multiline(dev_dependencies)
        }

    pip_metadata["build-system"] = {
        "requires": tu.format_list_multiline(["setuptools", "wheel"]),
        "build-backend": "setuptools.build_meta",
    }

    # Preserve all tool configurations except `tool.poetry`
    pip_metadata["tool"] = {}
    for tool_key in original_toml.get("tool", {}):
        if tool_key != "poetry":
            pip_metadata["tool"][tool_key] = original_toml["tool"][tool_key]

    # If using src layout, ensure setuptools recognizes it
    if packages:
        pip_metadata["tool"]["setuptools"] = {"packages": packages}

    return pip_metadata


# def write_to_pyproject_toml(pip_metadata: dict, path: Path):
#     """Writes the converted metadata to a new TOML file with proper formatting."""
#     with path.open(mode="w") as f:
#         tomlkit.dump(pip_metadata, f)


def main():
    """Converts a Poetry-based pyproject.toml to a pip-compatible version."""
    parser = argparse.ArgumentParser(description="Convert Poetry pyproject.toml to pip-compatible format.")
    parser.add_argument("-i", "--input", type=Path, required=True, help="Path to the Poetry pyproject.toml file.")
    parser.add_argument("-o", "--output", type=Path, required=True,
                        help="Path to save the converted pip-compatible pyproject.toml file.")
    args = parser.parse_args()

    toml_doc = tu.get_toml_doc(path=args.input)
    poetry_metadata = toml_doc["tool"]["poetry"]
    pip_metadata = create_pip_metadata(poetry_metadata=poetry_metadata, original_toml=toml_doc)
    tu.write_to_pyproject_toml(metadata=pip_metadata, path=args.output)

    print(f"✅ Successfully converted {args.input} to {args.output}!")

if __name__ == "__main__":
    main()
