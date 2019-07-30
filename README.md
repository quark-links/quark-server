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

## Overview

- **Free.** VH7 is not only free to use on the [official instance](https://vh7.uk) but is also free to download and run
for yourself.
- **Open Source.** All of VH7's source code is available here for the community to take a look under the hood. _We also
accept community contributions, just open a pull request!_
- **Multi-purpose.** Unlike other mainstream URL shorteners, VH7 also provides file sharing and a pastebin also with short
links.

## Installation

### Docker _(recommended)_

A ready for production Docker image is available at [jake-walker/vh7](https://cloud.docker.com/u/jakewalker/repository/docker/jakewalker/vh7).

```shell script
docker run --detach \
           --name vh7 \
           --publish 8080:8080 \
           --restart always \
           jake-walker/vh7:latest
```

#### Build Docker Image Manually

_This command requires Java JDK 8 or later and Apache Maven._

```shell script
mvn clean package dockerfile:build
```

The built Docker image is saved as `jake-walker/vh7:1.x.x`. You can then use the same command above to run the newly built
Docker image.

_Additional help on Dockerfile generation is available [here](https://github.com/spotify/dockerfile-maven)._

### Ordinary Java

_This command requires Java JDK 8 or later and Apache Maven._

```shell script
mvn clean package
java -jar ./target/vh7-1.x.x.jar
```

## Development

_VH7 requires Java JDK 8 or later and Apache Maven._

First clone the repository:

```shell script
git clone https://github.com/jake-walker/vh7.git
```

Now open the project in your favourite editor.

- Run `mvn verify` to run tests before submitting changes.