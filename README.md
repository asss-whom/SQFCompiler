# SQFCompiler

## Introduction

SQFCompiler is a Python program that translates Python code into SQF (Script Query Format) code. It aims to provide a bridge between the two languages, enabling developers to write scripts in Python and then compile them into SQF for use in environments that support SQF, such as Arma 3.

**Note:** This is a highly experimental version of the compiler and currently supports only a very limited subset of Python syntax.

## Installation

To install SQFCompiler, you need to have Python 3.11 installed on your system. This program has not been tested on other Python versions, so using it with other versions is not recommended.

Clone or download this repository, and then use pip to install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Once the dependencies are installed, you can use the following command to compile a Python file into SQF:

```bash
py main.py fileIn.py fileOut.sqf
```

Where `fileIn.py` is the input Python file you want to compile, and `fileOut.sqf` is the output file where the compiled SQF code will be saved.

## Limitations

Please note the following limitations of the current version of SQFCompiler:

1. **Python Version**: This program has only been tested with Python 3.11. Using it with other Python versions may result in unexpected behavior or errors.
2. **Supported Syntax**: SQFCompiler currently supports only a very limited subset of Python syntax. More complex features and constructs may not be recognized or translated correctly.

## License

SQFCompiler is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
