<h1 align="center">
	<img src="https://github.com/jake-walker/vh7-app/blob/main/static/img/vh7.png?raw=true" style="height: 4em;" alt="VH7 Logo">
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
	<a href="https://github.com/jake-walker/vh7/actions?query=workflow%3Aci" target="_blank"><img alt="Build Status" title="Build Status" src="https://img.shields.io/github/workflow/status/jake-walker/vh7/ci/main"></a>
    <a href="https://deepsource.io/gh/jake-walker/vh7/?ref=repository-badge" target="_blank"><img alt="DeepSource" title="DeepSource" src="https://deepsource.io/gh/jake-walker/vh7.svg/?label=active+issues&show_trend=true"/></a>
    <img alt="License" title="Licence" src="https://img.shields.io/github/license/jake-walker/vh7">
    <img alt="Pipenv Python version" src="https://img.shields.io/github/pipenv/locked/python-version/jake-walker/vh7/main">
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

- **Free.** VH7 is not only free to use on the [official instance](https://vh7.uk) but is also free to download and run
for yourself.
- **Open Source.** All of VH7's source code is available here for the community to take a look under the hood. _We also
accept community contributions, just open a pull request!_
- **Multi-purpose.** Unlike other mainstream URL shorteners, VH7 also provides file sharing and a pastebin also with short
links.

## Getting Started

The recommended way of deploying is with [Docker](#docker), however, if you wish to deploy it with something else, there are instructions [here](https://fastapi.tiangolo.com/deployment/) on how to do so.

An OAuth2 server is also needed. If you are going the self-hosting route, you can go for something like [FusionAuth](https://fusionauth.io/), or if you want something hosted, you could use [Auth0](https://auth0.com/) or [Okta](https://www.okta.com/).

Configuration can be done inside the `settings.toml` file (or in `.secrets.toml` which is ignored by Git) or via environment variables with the format `VH7_[SECTION]__[NAME]`.

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
           -e VH7_DATABASE=mysql+mysqldb://username:password@hostname/database
           -e VH7_UPLOADS__MIN_AGE=30
           -e VH7_UPLOADS__MAX_AGE=90
           -e VH7_UPLOADS__MAX_SIZE=256
           -v vh7_uploads:/uploads
           -p 80:8000
           jakewalker/vh7:latest
```

#### Manually Building Docker Image

```
docker build -t jakewalker/vh7 .
```

The built Docker image is saved as `vh7`. You can use then use the same command as above to run the newly built Docker image.

## Development

These instructions go over the method to setup a development environment for VH7. These instructions **should not** be used for a production setup of VH7.

### Prerequisites

- [Python 3.8](https://www.python.org/downloads/) (or any other version of Python 3)
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
