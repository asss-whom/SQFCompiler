# MIT License

# Copyright (c) 2024 asss-whom

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys

from utils import to_sqf, log


def main() -> None:
    if sys.version_info.minor != 11 or sys.version_info.major != 3:
        log.warning(
            "This program has only been tested on Python version 3.11. "
            "Running it on other versions is at your own risk."
        )

    if len(sys.argv) < 3:
        log.info("📜 Usage: main.py fileIn.py fileOut.sqf")
        return None

    fileIn = sys.argv[1]
    fileOut = sys.argv[2]

    log.info(f"{fileIn} -> {fileOut}")
    with open(fileIn) as f:
        source = f.read()
    result = to_sqf(source)
    with open(fileOut, "w") as f:
        f.write(result)
    log.info("Success!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.exception(e)
