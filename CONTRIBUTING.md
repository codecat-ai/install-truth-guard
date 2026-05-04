# Contributing

Thank you for helping improve install-truth-guard.

## Development

Use a local clone and an isolated Python environment. Run the focused tests for
the behavior you change, then run the full suite before opening a pull request.

```sh
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

## Guidelines

- Keep tests offline by using fake registry clients.
- Do not execute commands parsed from README files.
- Use English comments and commit messages.
- Keep documentation truthful about publication status.
