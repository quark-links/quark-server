<h1 align="center">
	<img src="https://github.com/quark-links/quark-app/blob/main/static/img/vh7.png?raw=true" style="height: 4em;" alt="VH7 Logo">
</h1>

<h3 align="center">
	A free and open source <u>URL shortening</u>, <u>file sharing</u> and <u>pastebin</u> service.
</h3>

<p align="center">
	<a href="https://github.com/quark-links/quark-server/actions?query=workflow%3Aci" target="_blank"><img alt="Build Status" title="Build Status" src="https://img.shields.io/github/workflow/status/quark-links/quark-server/main"></a>
    <a href="https://deepsource.io/gh/quark-links/quark-server/?ref=repository-badge" target="_blank"><img alt="DeepSource" title="DeepSource" src="https://deepsource.io/gh/quark-links/quark-server.svg/?label=active+issues&show_trend=true"/></a>
    <img alt="License" title="Licence" src="https://img.shields.io/github/license/quark-links/quark-server">
    <img alt="Pipenv Python version" src="https://img.shields.io/github/pipenv/locked/python-version/quark-links/quark-server/main">
</p>

<!-- TOC -->

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Deployment Notes](#deployment-notes)
    - [Docker](#docker)
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

- **Free.** Quark is not only free to use on the [official instance](https://vh7.uk) but is also free to download and run
for yourself.
- **Open Source.** All of Quark's source code is available here for the community to take a look under the hood. _We also
accept community contributions, just open a pull request!_
- **Multi-purpose.** Unlike other mainstream URL shorteners, Quark also provides file sharing and a pastebin also with short
links.

## Getting Started

The recommended way of deploying is with [Docker](#docker), however, if you wish to deploy it with something else, there are instructions [here](https://fastapi.tiangolo.com/deployment/) on how to do so.

An OAuth2 server is also needed. If you are going the self-hosting route, you can go for something like [FusionAuth](https://fusionauth.io/), or if you want something hosted, you could use [Auth0](https://auth0.com/) or [Okta](https://www.okta.com/).

Configuration can be done inside the `settings.toml` file (or in `.secrets.toml` which is ignored by Git) or via environment variables with the format `QUARK_[SECTION]__[NAME]`.

### Deployment Notes

- It is recommended to use a reverse proxy such as [Nginx](https://www.nginx.com/) or [Caddy](https://caddyserver.com/) between the internet and the instance of Quark.
- It is recommended to use a MySQL database instead of the default SQLite database.

### Docker

The suggested way of running Quark is through Docker. Docker images are automatically built for every version of Quark.

```
docker volume create quark_uploads
docker run --detach \
           --name quark \
           --restart always \
           -e QUARK_DATABASE=mysql+mysqldb://username:password@hostname/database
           -e QUARK_UPLOADS__MIN_AGE=30
           -e QUARK_UPLOADS__MAX_AGE=90
           -e QUARK_UPLOADS__MAX_SIZE=256
           -v quark_uploads:/uploads
           -p 80:8000
           docker.pkg.github.com/quark-links/quark-server/server:latest
```

#### Manually Building Docker Image

```
docker build -t docker.pkg.github.com/quark-links/quark-server/server .
```

The built Docker image is saved as `docker.pkg.github.com/quark-links/quark-server/server`. You can use then use the same command as above to run the newly built Docker image.

## Development

These instructions go over the method to setup a development environment for Quark. These instructions **should not** be used for a production setup of Quark.

### Prerequisites

- [Python 3.8](https://www.python.org/downloads/) (or any other version of Python 3)
- [Pipenv](https://github.com/pypa/pipenv) (for managing dependencies and a virtual environment)

### Installation

Clone the repository

```
git clone https://github.com/quark-links/quark-server
```

Install the dependencies

```
pipenv install --dev
```

Then setup the database with the latest schema

```
pipenv run alembic db upgrade
```

Then finally, run

```
pipenv run python app.py
```

Open a browser to <https://localhost:5000/>.

## Running Tests

### Code Style

Code Style is checked by [mypy](https://mypy.readthedocs.io/en/stable/).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please run tests and mypy before committing.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
