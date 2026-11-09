
# Contributing Guidelines

## 1. Code Style and Naming Conventions

All Python code must follow the PEP 8 style guidelines to ensure readability and consistency.

- Use `snake_case` for variables and function names.
- Use `PascalCase` for class names.
- Use meaningful and descriptive names.
- Keep functions focused on a single responsibility.
- Use type hints where appropriate.
- Include docstrings for functions explaining their purpose.

## 2. Code Quality

To maintain code quality, the following tools should be used:

- Ruff: to identify code quality issues and enforce consistent formatting.
- Pytest: to run automated tests and verify that functions behave as expected.

Code should be checked with Ruff and tested with Pytest before being submitted.

## 3. Testing

- New functionality should include relevant tests.
- Tests should cover normal scenarios and potential errors.
- Tests must use synthetic data only.
- All tests should pass before a Pull Request is submitted.

## 4. Dependency Management

- Project dependencies must be documented in `requirements.txt`.
- Package versions should be pinned to ensure reproducibility.
- New dependencies should only be added when necessary.
- Developers must update `requirements.txt` when adding or changing dependencies.

## 5. Git Workflow

- Create a separate branch for each new feature or bug fix.
- Use clear and descriptive commit messages.
- Changes should be reviewed through a Pull Request before being merged into the main branch.
- Avoid committing temporary files, credentials or sensitive information.

## 6. Security and Data Protection

- Only synthetic data should be used during development and testing.
- Never store passwords, API keys or other secrets in source code.
- Sensitive information must not be committed to the repository.
- Validate input data before processing it.

## 7. Documentation

- Update the README.md when project functionality or setup instructions change.
- Document significant technical decisions.
- Keep documentation clear and understandable for both technical and non-technical contributors.
