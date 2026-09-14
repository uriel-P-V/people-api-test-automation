# People API Test Automation

Automated REST API tests built with Python, Pytest, Requests, and AssertPy. This project was developed while following the Python API Testing course from Automation Hacks / Test Automation University and adapted to a modern Windows + Python environment.

## Overview

This project demonstrates how to automate tests for a REST API using Python. The test suite covers the main CRUD operations and uses Pytest fixtures to handle test data and setup/teardown activities.

The API under test is the **People API**, while this repository contains the automated test framework.

## Technologies

- **Python 3.13**
- **Pytest 9.1.1**
- **Requests** — HTTP requests to the REST API
- **AssertPy** — fluent and readable assertions
- **Pipenv** — dependency and virtual-environment management
- **Git / GitHub** — version control

## Test Coverage

| Test | Description |
|---|---|
| `test_get_people` | Verifies that the API returns people successfully with HTTP 200. |
| `test_post_person` | Creates a new person and verifies HTTP 204. |
| `test_delete_person` | Creates a dedicated test person and verifies it can be deleted with HTTP 200. |
| `test_put_person` | Creates a test person, updates it, and verifies HTTP 200. |
| `test_new_person` | Verifies data created through the `new_person` fixture. |

## Pytest Fixtures

The project uses fixtures to avoid duplicating test setup logic.

### `new_person`

Creates a unique person before the test using `uuid4()`, obtains its `person_id`, and removes the person during teardown.

This fixture demonstrates the Pytest `yield` pattern:

```text
Setup
  ↓
Create test data
  ↓
yield
  ↓
Run test
  ↓
Teardown
  ↓
Delete test data
```

### `person_to_delete`

Creates a dedicated person for the DELETE test and provides its `person_id` to the test.

## Project Structure

```text
people-api-test-automation/
│
├── tests/
│   ├── config.py
│   └── test_people.py
│
├── .gitignore
├── Pipfile
├── Pipfile.lock
└── README.md
```

## API Configuration

The base API URL is defined in `tests/config.py`:

```python
BASE_URI = "http://127.0.0.1:5000/api/people"
```

The People API must be running locally before executing the tests.

## Installation

Clone the repository:

```bash
git clone https://github.com/uriel-P-V/people-api-test-automation.git
cd people-api-test-automation
```

Install the project dependencies with Pipenv:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

## Running the Tests

Make sure the People API is running on:

```text
http://127.0.0.1:5000
```

Then execute:

```bash
pytest
```

Expected result:

```text
5 passed
```

## API Operations Tested

The test suite currently exercises these REST operations:

```text
GET     /api/people
POST    /api/people
PUT     /api/people/{id}
DELETE  /api/people/{id}
```

## What This Project Demonstrates

- REST API test automation with Python
- HTTP requests using `requests`
- Response status-code validation
- JSON request and response handling
- Test data generation with UUIDs
- Pytest fixtures
- Setup and teardown using `yield`
- CRUD API testing
- Separation between the API and the automated test project
- Dependency management with Pipenv

## Author

**Uriel Alejandro Perez Valdovinos**

GitHub: https://github.com/uriel-P-V
