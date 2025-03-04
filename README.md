# pyprojectconverter

Utility for converting between pyproject.toml formats for poetry and pip


## Usage

### Clone the project and change directory
```shell
git clone https://github.com/duanegoodner/pyprojectconverter
cd pyprojectconverter
```

### Converting from Pip Format to Poetry Format

#### Command Line Help
Run:
```shell
python pyprojectconverter/pip_to_poetry.py --help
```
Output:
```shell
usage: pip_to_poetry.py [-h] -i INPUT -o OUTPUT

Convert pip pyproject.toml to Poetry-compatible format.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the pip pyproject.toml file.
  -o OUTPUT, --output OUTPUT
                        Path to save the converted Poetry-compatible pyproject.toml file.
```

#### Example

Run:
```shell
python pyprojectconverter/pip_to_poetry.py -i data/orig_for_pip.toml -o converted_to_poetry.toml
```
Output:
```shell
✅ Successfully converted data/orig_for_pip.toml to converted_to_poetry.toml!
```

Then open file `converted_to_poetry.toml` and compare it to `./data/orig_for_poetry.toml`. Their content should match, but may have different section orders.

### Converting from Pip Format to Poetry Format

#### Command Line Help
Run:
```shell
python pyprojectconverter/poetry_to_pip.py --help
```
Output:
```shell
usage: poetry_to_pip.py [-h] -i INPUT -o OUTPUT

Convert Poetry pyproject.toml to pip-compatible format.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the Poetry pyproject.toml file.
  -o OUTPUT, --output OUTPUT
                        Path to save the converted pip-compatible pyproject.toml file.
```

#### Example

Run:
```shell
 python pyprojectconverter/poetry_to_pip.py -i data/orig_for_poetry.toml -o converted_to_pip.toml
```
Output:
```shell
✅ Successfully converted data/orig_for_poetry.toml to converted_to_pip.toml!
```

The content of `converted_to_pip.toml` should match `./data/orig_for_pip.toml` except for section ordering.



