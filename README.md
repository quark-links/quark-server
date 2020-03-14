<h1 align="center">
	<img src="static/img/logo.png" style="height: 4em;" alt="VH7 Logo">
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

<!-- TOC -->

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Deployment Notes](#deployment-notes)
    - [Docker](#docker)
        - [Tags](#tags)
        - [Manually Building Docker Image](#manually-building-docker-image)
- [Development](#development)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Running Tests](#running-tests)
    - [Code Style](#code-style)
- [Contributing](#contributing)
- [License](#license)

<!-- /TOC -->

## Overview

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/29ecbb890baa4834a6b6ed5091d93eb6)](https://app.codacy.com/manual/jake-walker/vh7?utm_source=github.com&utm_medium=referral&utm_content=jake-walker/vh7&utm_campaign=Badge_Grade_Dashboard)

- **Free.** VH7 is not only free to use on the [official instance](https://vh7.uk) but is also free to download and run
for yourself.
- **Open Source.** All of VH7's source code is available here for the community to take a look under the hood. _We also
accept community contributions, just open a pull request!_
- **Multi-purpose.** Unlike other mainstream URL shorteners, VH7 also provides file sharing and a pastebin also with short
links.

## Getting Started

The recommended way of deploying is with [Docker](#docker), however, if you wish to deploy it with something else, there are instructions [here](http://docs.gunicorn.org/en/latest/deploy.html) on how to do so.

Check the [configuration page](https://github.com/jake-walker/vh7/wiki/Configuration) to see the different settings that VH7 can be configured with.

### Deployment Notes

- It is recommended to use a reverse proxy such as [Nginx](https://www.nginx.com/) or [Caddy](https://caddyserver.com/) between the internet and the instance of VH7.
- It is recommended to use a MySQL database instead of the default SQLite database.

### Docker

The suggested way of running VH7 is through Docker. Docker images are automatically built for every version of VH7 at [`jakewalker/vh7`](https://hub.docker.com/r/jakewalker/vh7).

```
docker volume create vh7_uploads
docker run --detach \
           --name vh7 \
           --restart always \
           -e VH7_DB_CONNECTION_STRING=mysql+mysqldb://username:password@hostname/database
           -e VH7_UPLOAD_FOLDER=/uploads
           -e VH7_SECRET=F6yZv5Xy8TBlYGkBs7P2wXlZqFAR3c
           -e VH7_SALT=wIkikFWxhAOV8O39B2JRCuyZqKQ8U1
           -e VH7_UPLOAD_MIN_AGE=30
           -e VH7_UPLOAD_MAX_AGE=90
           -e VH7_UPLOAD_MAX_SIZE=256
           -v vh7_uploads:/uploads
           -p 80:8000
           jakewalker/vh7:latest
```

#### Tags

The image [`jakewalker/vh7`](https://hub.docker.com/r/jakewalker/vh7) has the following tags:

- **`latest` → All** - Built on every commit to `master`, it should be stable to use in a production environment, but not as stable as the tags below.
- **`0.1`, `0.1.1` → Stable** - All version tags are more stable than `latest` and should be used where you would like the most stable version of VH7 as possible.

#### Manually Building Docker Image

```
docker build -t jakewalker/vh7 .
```

The built Docker image is saved as `vh7`. You can use then use the same command as above to run the newly built Docker image.

## Development

These instructions go over the method to setup a development environment for VH7. These instructions **should not** be used for a production setup of VH7.

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
pipenv install --dev
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
