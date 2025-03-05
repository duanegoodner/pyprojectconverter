# convertpytoml

*A simple utility to convert between Poetry and pip `pyproject.toml` formats.*


## 📥 Installation & Setup

### Clone the repository and navigate to the project directory
```shell
git clone https://github.com/duanegoodner/pyprojectconverter
cd pyprojectconverter
```

## ⚡ Usage

### 🔄 Convert from pip format to Poetry format

#### 📌 Command Line Help
Run:
```shell
python pyprojectconverter/pip_to_poetry.py --help
```
Expected output:
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

#### ⚙️ Example Conversion

Convert a pip-style `pyproject.toml` to Poetry format:
```shell
python pyprojectconverter/pip_to_poetry.py -i data/orig_for_pip.toml -o converted_to_poetry.toml
```
Expected output:
```shell
✅ Successfully converted data/orig_for_pip.toml to converted_to_poetry.toml!
```

Now, compare `converted_to_poetry.toml` with `data/orig_for_poetry.toml`. The structure may be reordered, but the content should be equivalent.

### 🔁 Convert from Poetry format to pip format

#### 📌 Command Line Help
Run:
```shell
python pyprojectconverter/poetry_to_pip.py --help
```
Expected output:
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

#### ⚙️ Example Conversion

Run:
```shell
 python pyprojectconverter/poetry_to_pip.py -i data/orig_for_poetry.toml -o converted_to_pip.toml
```
Expected Output:
```shell
✅ Successfully converted data/orig_for_poetry.toml to converted_to_pip.toml!
```

Now, compare `converted_to_pip.toml` with `data/orig_for_pip.toml`. The structure may be reordered, but the content should be equivalent.

## ℹ️ Notes

- The script does not modify the original file. Instead, it saves the converted version to the specified output path.
- Converted files may have different section ordering but retain the same content.
- Supports both dependency conversion and source layout detection (src-based or flat layouts).



