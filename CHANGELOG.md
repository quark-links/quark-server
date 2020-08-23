# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Image and video previews on uploaded files.
- Changelog page.

### Changed

- Bytecode and buffering is disabled in Dockerfile.
- Python 3.8 is now used by default instead of Python 3.7.
- Now using hCaptcha instead of Google reCAPTCHA.

### Fixed

- "SQL Server Gone Away" fix.
- Hide show API QR code button in account page if no API key is assigned to the account.

## [0.5.0] - 2020-04-25

### Added

- Google reCAPTCHA on login and registration pages.

### Fixed

- CORS headers are now correctly added to just API routes.
