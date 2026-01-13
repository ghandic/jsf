# Automated Release Process

This repository uses an automated release process that triggers when code is merged to the `main` branch.

## How It Works

1. **Conventional Commits**: The automation analyzes commit messages since the last release to determine the next version number.

2. **Version Calculation**: Based on commit message prefixes:
   - `feat:` or `feat(scope):` → **minor** version bump (e.g., 0.11.2 → 0.12.0)
   - `fix:` or `fix(scope):` → **patch** version bump (e.g., 0.11.2 → 0.11.3)
   - `BREAKING CHANGE:` or `feat!:` → **major** version bump (e.g., 0.11.2 → 1.0.0)
   - Other conventional commits (`chore:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`) → **patch** version bump

3. **Automated Steps**: When merging to `main`:
   - The release workflow analyzes commits since the last tag
   - Determines the appropriate version bump
   - Updates the version in `jsf/BUILD`
   - Creates a git commit with the version bump (marked with `[skip ci]`)
   - Creates a GitHub release with an auto-generated changelog
   - The GitHub release triggers existing workflows to:
     - Publish to PyPI
     - Deploy documentation to GitHub Pages

## Commit Message Format

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Examples

**Feature (minor version bump):**
```
feat: add support for custom data providers
```

**Bug fix (patch version bump):**
```
fix: correct validation for nested objects
```

**Breaking change (major version bump):**
```
feat!: redesign API interface

BREAKING CHANGE: The generate() method now returns a dict instead of a string
```

**Documentation (patch version bump):**
```
docs: update installation instructions
```

**Chore (patch version bump):**
```
chore: update dependencies
```

## Manual Release (if needed)

If you need to create a release manually:

1. Update the version in `jsf/BUILD`
2. Commit the change: `git commit -m "chore: bump version to X.Y.Z [skip ci]"`
3. Push to main: `git push origin main`
4. Create a GitHub release manually with tag `vX.Y.Z`

The `[skip ci]` marker prevents the automated release workflow from running again.

## Benefits

- ✅ Consistent versioning based on semantic versioning principles
- ✅ Automated changelog generation
- ✅ No manual version management needed
- ✅ Immediate release after merge to main
- ✅ Clear commit history with conventional commits
- ✅ Reduced human error in the release process

## Notes

- The workflow only runs on pushes to the `main` branch
- If no conventional commit messages are found, no release is created
- The Python package tests workflow skips on `[skip ci]` commits to avoid redundant builds
- Existing release workflows (PyPI publish, docs deploy) remain unchanged and are triggered by the created GitHub release
