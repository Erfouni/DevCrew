# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-10-21

### Added
- Installable package with a `devcrew` command (`pip install -e .`).
- `--output-dir` and `--model` options, plus `--version`.
- Unit tests that check pipeline wiring and validate `sample_output/` against the schemas,
  without calling an LLM.
- CI on Python 3.10–3.13 (lint, tests, package build) and a PyPI release workflow.
- MIT license, contributing guide, security policy, issue and PR templates.

### Changed
- Schemas now constrain QA verdicts, review severities, review verdicts and 1–10 scores, so
  malformed agent output is rejected instead of passed downstream.

### Fixed
- `--output-dir` refuses absolute paths and `..`. CrewAI only writes to relative paths and would
  otherwise silently turn `/tmp/out` into `./tmp/out`.

## 0.0.1 - 2026-08-18

- First version: Project Manager → Developer → QA Tester → Code Reviewer pipeline on CrewAI.

[Unreleased]: https://github.com/agrvasu05/DevCrew/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/agrvasu05/DevCrew/releases/tag/v0.1.0
