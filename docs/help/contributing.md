# Contributing

Contributions are welcome, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

## Environment setup

Nothing easier!

Fork and clone the repository, then install [`pants`](https://www.pantsbuild.org/2.18/docs/getting-started/installing-pants)

```bash
# Install `pants` on macos
brew install pantsbuild/tap/pants

# Export the virtual environment for IDE
pants export --py-resolve-format=symlinked_immutable_virtualenv --resolve=python-default
```

That's it!

You now have the dependencies installed.

## Development

As usual:

1. create a new branch: `git checkout -b feature-or-bugfix-name`
1. edit the code and/or the documentation

**Before committing:**

1. Ensure to run `pants fmt ::` from the root directory to format all of the code in the repo before PR submission.
2. Follow our [commit message convention](#commit-message-convention)

If you are unsure about how to fix or ignore a warning,
just let the continuous integration fail,
and we will help you during review.

Don't bother updating the changelog, we will take care of this.

## Commit message convention

Commits messages must follow the
[Angular style](https://gist.github.com/stephenparish/9941e89d80e2bc58a153#format-of-the-commit-message):

```txt
<type>[(scope)]: Subject

[Body]
```

Scope and body are optional. Type can be:

- `build`: About packaging, building wheels, etc.
- `chore`: About packaging or repo/files management.
- `ci`: About Continuous Integration.
- `docs`: About documentation.
- `feat`: New feature.
- `fix`: Bug fix.
- `perf`: About performance.
- `refactor`: Changes which are not features nor bug fixes.
- `style`: A change in code style/format.
- `tests`: About tests.

**Subject (and body) must be valid Markdown.**
If you write a body, please add issues references at the end:

```txt
Body.

References: #10, #11.
Fixes #15.
```
