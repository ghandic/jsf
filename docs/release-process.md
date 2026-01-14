# Automated Release Process

This repository supports both automated and manual release processes.

## Automated Releases

The automation triggers automatically when code is merged to the `main` branch.

### How It Works

1. **Conventional Commits**: The automation analyzes commit messages since the last release to determine the next version number.

2. **Version Calculation**: Based on commit message prefixes:
   - `feat:` or `feat(scope):` → **minor** version bump (e.g., 0.11.2 → 0.12.0)
   - `fix:` or `fix(scope):` → **patch** version bump (e.g., 0.11.2 → 0.11.3)
   - `BREAKING CHANGE:` or `feat!:` → **major** version bump (e.g., 0.11.2 → 1.0.0)
   - Other conventional commits (`chore:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`) → **patch** version bump
   - **Any other commits (non-conventional)** → **patch** version bump (default behavior)

3. **Automated Steps**: When merging to `main`:
   - The release workflow analyzes commits since the last tag
   - Determines the appropriate version bump
   - Updates the version in `jsf/BUILD`
   - Creates a git commit with the version bump (marked with `[skip ci]`)
   - Creates a GitHub release with an auto-generated changelog
   - The GitHub release triggers existing workflows to:
     - Publish to PyPI
     - Deploy documentation to GitHub Pages

## Manual Releases

You can manually trigger a release and specify the exact version number.

### How to Trigger a Manual Release

1. **On GitHub Web/Mobile**:
   - Go to the "Actions" tab
   - Select "Automated Release" workflow
   - Click "Run workflow"
   - Choose options:
     - **Version**: Enter a specific version (e.g., `1.2.3`) to release that exact version, or leave empty for automatic versioning
     - **Bump type**: If version is empty, choose `major`, `minor`, `patch`, or `auto` (analyzes commits)
   - Click "Run workflow"

2. **Using GitHub CLI**:
   ```bash
   # Release a specific version
   gh workflow run .github/workflows/release.yaml -f version=1.2.3
   
   # Or specify bump type for automatic calculation
   gh workflow run .github/workflows/release.yaml -f bump_type=minor
   
   # Or use the workflow name
   gh workflow run "Automated Release" -f version=1.2.3
   ```

### When to Use Manual Releases

- **After merging a PR on mobile**: Accept the PR, then manually trigger the release with your chosen version
- **Hotfix releases**: Quickly release a specific version without analyzing commits
- **Version alignment**: Set a specific version to align with project milestones

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
- ✅ Default patch version bump ensures every merge creates a release

## Notes

- The workflow only runs on pushes to the `main` branch
- If there are no new commits since the last release, no new release is created
- **If commits don't follow conventional commit format, a patch version bump is applied by default**
- The Python package tests workflow skips on `[skip ci]` commits to avoid redundant builds
- Existing release workflows (PyPI publish, docs deploy) remain unchanged and are triggered by the created GitHub release
