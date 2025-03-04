from pathlib import Path
import tomlkit


def get_toml_doc(path: Path) -> tomlkit.TOMLDocument:
    """Reads a TOML file and returns a TOMLDocument."""
    with path.open(mode="r") as f:
        return tomlkit.loads(f.read())


def get_poetry_metadata(toml_doc: tomlkit.TOMLDocument) -> dict:
    """Extracts the Poetry metadata from the TOML document."""
    return toml_doc["tool"]["poetry"]


def convert_version_specifier(version: str) -> str:
    """
    Converts Poetry version specifiers to Pip equivalents.
    Example: "^1.2.3" -> ">=1.2.3,<2.0.0"
    """
    if version == "*":
        return ""
    elif version.startswith("^"):
        base_version = version[1:]
        major, *rest = base_version.split(".")
        next_major = str(int(major) + 1)
        return f">={base_version},<{next_major}.0.0"
    elif version.startswith("~"):
        base_version = version[1:]
        major, minor, *rest = base_version.split(".")
        next_minor = str(int(minor) + 1) if minor else "0"
        return f">={base_version},<{major}.{next_minor}.0"
    return version  # Otherwise, return as-is


def get_dependencies(poetry_metadata: dict) -> list:
    """Extracts and converts dependencies from Poetry to Pip format."""
    return [
        f"{pkg}{convert_version_specifier(ver)}"
        for pkg, ver in poetry_metadata["dependencies"].items()
        if pkg.lower() != "python"
    ]


def get_dev_dependencies(poetry_metadata: dict) -> list:
    """Extracts and converts dev dependencies from Poetry to Pip format."""
    if "group" in poetry_metadata and "dev" in poetry_metadata["group"]:
        return [
            f"{pkg}{convert_version_specifier(ver)}"
            for pkg, ver in poetry_metadata["group"]["dev"]["dependencies"].items()
        ]
    return []


def create_pip_metadata(poetry_metadata: dict) -> dict:
    """Converts Poetry metadata to Pip-compatible pyproject.toml format."""
    dependencies = get_dependencies(poetry_metadata)
    dev_dependencies = get_dev_dependencies(poetry_metadata)

    pip_metadata = {
        "project": {
            "name": poetry_metadata["name"],
            "version": poetry_metadata["version"],
            "description": poetry_metadata["description"],
            "authors": poetry_metadata["authors"],
            "dependencies": dependencies,
        },
        "build-system": {
            "requires": ["setuptools", "wheel"],
            "build-backend": "setuptools.build_meta",
        },
    }

    if dev_dependencies:
        pip_metadata["project"]["optional-dependencies"] = {"dev": dev_dependencies}

    return pip_metadata


def write_to_pyproject_toml(pip_metadata: dict, path: Path):
    """Writes the converted metadata to a new pyproject.toml file with proper formatting."""
    toml_doc = tomlkit.document()

    # Set up the [project] section
    project_section = tomlkit.table()
    project_section["name"] = pip_metadata["project"]["name"]
    project_section["version"] = pip_metadata["project"]["version"]
    project_section["description"] = pip_metadata["project"]["description"]
    project_section["authors"] = pip_metadata["project"]["authors"]

    # Format dependencies as a multi-line array
    project_section["dependencies"] = tomlkit.array(pip_metadata["project"]["dependencies"]).multiline(True)

    # Handle optional dependencies
    if "optional-dependencies" in pip_metadata["project"]:
        optional_deps = tomlkit.table()
        for group, deps in pip_metadata["project"]["optional-dependencies"].items():
            optional_deps[group] = tomlkit.array(deps).multiline(True)
        project_section["optional-dependencies"] = optional_deps

    toml_doc["project"] = project_section

    # Set up the [build-system] section
    build_system = tomlkit.table()
    build_system["requires"] = tomlkit.array(pip_metadata["build-system"]["requires"]).multiline(True)
    build_system["build-backend"] = pip_metadata["build-system"]["build-backend"]
    toml_doc["build-system"] = build_system

    # Write the formatted TOML file
    with path.open(mode="w") as f:
        f.write(tomlkit.dumps(toml_doc))


def main(poetry_toml_path: Path, new_pip_toml_path: Path):
    """Main function to read, convert, and write the new pyproject.toml."""
    toml_doc = get_toml_doc(path=poetry_toml_path)
    poetry_metadata = get_poetry_metadata(toml_doc)
    pip_metadata = create_pip_metadata(poetry_metadata=poetry_metadata)
    write_to_pyproject_toml(pip_metadata=pip_metadata, path=new_pip_toml_path)


if __name__ == "__main__":
    main(
        poetry_toml_path=Path("orig_toml_files") / "orig_for_poetry.toml",
        new_pip_toml_path=Path("converted_toml_files") / "converted_to_pip.toml",
    )
