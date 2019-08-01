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
	<a href="https://dev.azure.com/jakewalker/VH7/_build?definitionId=3"><img
        alt="Azure DevOps Build Status"
    	src="https://img.shields.io/azure-devops/build/jakewalker/c9dce4e0-e2bd-4041-bb56-2dc7e4d98c37/3/master?style=flat-square"></a>
</p>

## Overview

- **Free.** VH7 is not only free to use on the [official instance](https://vh7.uk) but is also free to download and run
for yourself.
- **Open Source.** All of VH7's source code is available here for the community to take a look under the hood. _We also
accept community contributions, just open a pull request!_
- **Multi-purpose.** Unlike other mainstream URL shorteners, VH7 also provides file sharing and a pastebin also with short
links.

## Installation

To run VH7 in production, you must set the following environment variables:

| Key                      | Example Production Value | Description |
| ------------------------ | ------------------------ | ----------- |
| `SPRING_PROFILES_ACTIVE` | `production`             | The Spring profile to use (`production` is designed for use in production). |
| `VH7_MYSQL_HOST`         | `127.0.0.1`              | The host of the MySQL database for VH7 to use. |
| `VH7_MYSQL_PORT`         | `3306`                   | The port of the MySQL database for VH7 to use. |
| `VH7_MYSQL_DATABASE`     | `vh7`                    | The database of the MySQL database for VH7 to use. |
| `VH7_MYSQL_USERNAME`     | `vh7-user`               | The username for the MySQL database for VH7 to use. |
| `VH7_MYSQL_PASSWORD`     | `password`               | The password for the MySQL database for VH7 to use. |
| `VH7_SHORTURL_SALT`      | `gh5489ghu47`            | The salt to be used for generating short URLs. _Any random string can be used._ **This must not change once an instance has been setup!(\*)**
| `VH7_URL`                | `https://vh7.uk/`        | The URL that users will access VH7 from. _This is used for building the short URLs._ |

<small>(\*) - If the salt is changed all short URLs will regenerate and old ones will no longer work. So it's best not to
change the salt!</small>

### Docker _(recommended)_

A ready for production Docker image is available at [jake-walker/vh7](https://cloud.docker.com/u/jakewalker/repository/docker/jakewalker/vh7).

```shell script
docker run --detach \
           --name vh7 \
           --publish 8080:8080 \
           --restart always \
           -e SPRING_PROFILES_ACTIVE="production" \
           -e VH7_MYSQL_HOST="127.0.0.1" \
           -e VH7_MYSQL_PORT="3306" \
           -e VH7_MYSQL_DATABASE="vh7" \
           -e VH7_MYSQL_USERNAME="vh7-user" \
           -e VH7_MYSQL_PASSWORD="password" \
           -e VH7_SHORTURL_SALT="gh5489ghu47" \
           -e VH7_URL="https://vh7.uk/" \
           jakewalker/vh7:latest
```

#### Build Docker Image Manually

_This command requires Java JDK 8 or later and Apache Maven._

```shell script
mvn clean package
docker build -t jakewalker/vh7 .
```

The built Docker image is saved as `jakewalker/vh7`. You can then use the same command above to run the newly built
Docker image.

_Additional help on Dockerfile generation is available [here](https://github.com/spotify/dockerfile-maven)._

### Ordinary Java

_This command requires Java JDK 8 or later and Apache Maven._

```shell script
# Build Application
mvn clean package

# Setup Environment
export SPRING_PROFILES_ACTIVE="production"
export VH7_MYSQL_HOST="127.0.0.1"
export VH7_MYSQL_PORT="3306"
export VH7_MYSQL_DATABASE="vh7"
export VH7_MYSQL_USERNAME="vh7-user"
export VH7_MYSQL_PASSWORD="password"
export VH7_SHORTURL_SALT="gh5489ghu47"
export VH7_URL="https://vh7.uk/"

# Run VH7
java -jar ./target/vh7-1.x.x.jar
```

## Development

_VH7 requires Java JDK 8 or later and Apache Maven._

First clone the repository:

```shell script
git clone https://github.com/jake-walker/vh7.git
```

Then build and run VH7:

_**Note:** Using the `development` Spring profile will store data in a temporary in-memory H2 database and use a development
salt and instance URL (see Installation section for more info). No environment variables are required._

```shell script
mvn clean package
java -jar ./target/vh7-1.x.x.jar -Dspring.profiles.active=development
```

Once you have made changes, feel free to open a pull request. Your code will be automatically checked by Azure Pipelines
and then reviewed.