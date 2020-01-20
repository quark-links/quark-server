<h1 align="center">
	VH7
</h1>

<h3 align="center">
	A free and open source <u>URL shortening</u>, <u>file sharing</u> and <u>pastebin</u> service.
</h3>

<p align="center">
	<strong>
		<a href="https://vh7.uk/">Website</a>
	</strong>
</p>
<p align="center">
	<a href="https://ci.jakewalker.xyz/jake-walker/vh7"><img
        alt="Build Status"
    	src="https://img.shields.io/drone/build/jake-walker/vh7/master?server=https%3A%2F%2Fci.jakewalker.xyz&style=flat-square"></a>
</p>

## Overview

- **Free.** VH7 is not only free to use on the [official instance](https://vh7.uk) but is also free to download and run
for yourself.
- **Open Source.** All of VH7's source code is available here for the community to take a look under the hood. _We also
accept community contributions, just open a pull request!_
- **Multi-purpose.** Unlike other mainstream URL shorteners, VH7 also provides file sharing and a pastebin also with short
links.

## Getting Started

**VH7 isn't ready for a production setup yet, so these instructions are for setting VH7 up in a development environment.**

### Prerequisites

- [Python 3.7](https://www.python.org/downloads/) (or any other version of Python 3)
- [Pipenv](https://github.com/pypa/pipenv) (for managing dependencies and a virtual environment)

### Installation

Clone the repository

```
git clone https://github.com/jake-walker/vh7
```

Install the dependencies

```
pipenv install
```

Then setup the database with the latest schema

```
pipenv run flask db upgrade
```

Then finally, run

```
pipenv run python app.py
```

Open a browser to <https://localhost:5000/>.

## Running Tests

### Code Style

Code Style is checked by [flake8](http://flake8.pycqa.org/en/latest/). Simply run `flake8` inside the virtual environment to run the checks.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please run tests and flake8 before committing.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
