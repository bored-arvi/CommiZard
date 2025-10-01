# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025/10/01

### Added

- `cp` command to copy the generated message to the clipboard.
- `commit` command to directly commit the generated message without editing.
- A unit test suite (currently 140 tests implemented, with 8 still failing).
- Argument parsing: `-h`, `--help`, `-v`, and `--version` are now supported.
- Added CHANGELOG.md to track notable changes.

### Changed

- Improved and updated `README.md`.
- Moved TODO items to GitHub issues.
- Added dynamic versioning: the project version is now centralized in
  `__init__.py`.
- Improved the diff sent to the LLM, allowing for more accurate commits with
  fewer tokens.
- Refactored significant parts of the codebase. This is still a work in
  progress, but the program’s flow is now cleaner and more maintainable.

### Fixed

- Fixed `gen` command crashing when user changes contained certain special
  Unicode characters. Changes containing any UTF-8 supported character are now
  handled correctly.

## [0.0.1-alpha] - 2025/09/16

### Added

- Basic functionality: `start`, `list`, `gen`, and `quit` commands.
- `README.md` to serve as a welcoming and getting started guide.
- `CONTRIBUTING.md` to help contributors get involved.
- MIT open source license.
- PyPI release: the package can now be installed with `pip install commizard`.

[Unreleased]: https://github.com/Chungzter/CommiZard/compare/v0.1.0...master

[0.1.0]: https://github.com/Chungzter/CommiZard/compare/v0.0.1a0...v0.1.0

[0.0.1-alpha]: https://github.com/Chungzter/CommiZard/releases/tag/v0.0.1a0
