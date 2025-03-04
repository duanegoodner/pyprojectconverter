import tomlkit

# Load the pip-compatible pyproject.toml
with open("pyproject_pip.toml", "r") as f:
    pip_pyproject = tomlkit.load(f)

# Extract metadata
project_metadata = pip_pyproject.get("project", {})

# Extract dependencies, ensuring they are formatted correctly
dependencies = project_metadata.get("dependencies", [])

# Extract dev dependencies (if available)
optional_dependencies = project_metadata.get("optional-dependencies", {})
dev_dependencies = optional_dependencies.get("dev", [])

# Create a Poetry-compatible pyproject.toml
poetry_pyproject = {
    "tool": {
        "poetry": {
            "name": project_metadata.get("name", ""),
            "version": project_metadata.get("version", ""),
            "description": project_metadata.get("description", ""),
            "authors": project_metadata.get("authors", []),
            "dependencies": {
                "python": "^3.11",  # Default to Python 3.11, adjust as needed
            },
            "group": {
                "dev": {
                    "dependencies": {}
                }
            } if dev_dependencies else {},
        }
    },
    "build-system": {
        "requires": ["poetry-core"],
        "build-backend": "poetry.core.masonry.api"
    }
}

# Add dependencies to Poetry format
for dep in dependencies:
    if "==" in dep:  # Handle fixed versions
        name, version = dep.split("==")
        poetry_pyproject["tool"]["poetry"]["dependencies"][name] = version
    else:
        poetry_pyproject["tool"]["poetry"]["dependencies"][dep] = "*"

# Add dev dependencies if they exist
if dev_dependencies:
    for dev_dep in dev_dependencies:
        if "==" in dev_dep:
            name, version = dev_dep.split("==")
            poetry_pyproject["tool"]["poetry"]["group"]["dev"]["dependencies"][name] = version
        else:
            poetry_pyproject["tool"]["poetry"]["group"]["dev"]["dependencies"][dev_dep] = "*"

# Write the new Poetry-compatible pyproject.toml
with open("pyproject_poetry.toml", "w") as f:
    tomlkit.dump(poetry_pyproject, f)

print("✅ Successfully converted to Poetry-compatible pyproject.toml!")
