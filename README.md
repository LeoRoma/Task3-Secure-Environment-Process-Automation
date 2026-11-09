
# Donor Readiness Automation

## 1. Project Overview

This project aims to demonstrate how Python can be used to automate donor data quality checks.

The solution will process synthetic donor records, identify potential data quality issues and generate a report containing the results.

The project is developed as part of a Level 6 apprenticeship.

## 2. Business Context

Accurate and up-to-date donor information is important for donor readiness activities.

Manually checking records can be time-consuming and may result in human errors.

This project explores how automation can make data quality checks more consistent, repeatable and efficient.

## 3. Technologies

The project uses the following technologies:

- Python 3.14
- pandas – data processing and validation
- pytest – automated testing
- Ruff – code quality and formatting
- GitHub Codespaces – development environment

## 4. Project Structure

```text
donor-readiness-automation/
├── .devcontainer/
│   └── devcontainer.json
├── README.md
├── CONTRIBUTING.md
├── requirements.txt
└── .gitignore
```

## 5. Environment Setup

The project uses GitHub Codespaces and a Dev Container to provide a consistent development environment.

Install the required dependencies using:

```bash
python -m pip install -r requirements.txt
```

## 6. Data Protection

Only synthetic data will be used for development and testing.

No real donor or patient information will be stored or processed as part of this demonstration.

The project will not connect to production or live systems.

## 7. Current Status

The initial development environment and dependency configuration have been prepared.

The next stage is to develop and test the Python automation script.

## 8. Coding Standards

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for coding standards, testing guidelines and contribution rules.
