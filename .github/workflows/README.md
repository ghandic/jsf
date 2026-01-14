# GitHub Actions Workflows

## Overview

This directory contains the GitHub Actions workflows for CI/CD automation.

## Workflows

### `python-package.yaml`
**Triggers:** Push to `main`, Pull requests to `main`

Runs tests, linting, and packaging for the Python package across multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14).

**Note:** Skips execution if commit message contains `[skip ci]`.

### `release.yaml`
**Triggers:** Push to `main`, Manual workflow dispatch

Automatically creates releases based on conventional commit messages, or allows manual version specification:

**Automatic Mode** (on push to main):
- Analyzes commits since last release
- Determines version bump (major/minor/patch)
- Updates version in `jsf/BUILD`
- Creates GitHub release with changelog
- Triggers `python-publish.yaml` and `mkdoc-gh-pages.yaml` via release creation

**Manual Mode** (workflow dispatch):
- Allows specifying exact version (e.g., `1.2.3`)
- Or choosing bump type (`major`, `minor`, `patch`, `auto`)
- Perfect for releasing after accepting PRs on mobile
- Maintainer controls the version, not PR author

See [Release Process Documentation](../../docs/release-process.md) for details.

### `python-publish.yaml`
**Triggers:** GitHub Release created

Publishes the package to PyPI when a release is created.

### `mkdoc-gh-pages.yaml`
**Triggers:** GitHub Release created, Manual workflow dispatch

Builds and deploys documentation to GitHub Pages.

## Versioning Strategy

The project uses semantic versioning with automated releases:
- `feat:` commits → **minor** version bump
- `fix:` commits → **patch** version bump
- Breaking changes (`feat!:`, `BREAKING CHANGE:`) → **major** version bump
- Other commits (non-conventional) → **patch** version bump (default)

## Development Notes

- Commits with `[skip ci]` in the message skip the test workflow
- The automated release workflow commits use `[skip ci]` to prevent recursive builds
- All workflows use Pants build system for consistent builds
