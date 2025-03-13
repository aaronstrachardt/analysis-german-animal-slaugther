# Tests

This directory contains tests for the German Animal Slaughter Analysis project.

## Running Tests

To run the tests, use the following command from the project root:

```bash
# Activate the virtual environment first
source venv/bin/activate  # On Linux/macOS
# OR
venv\Scripts\activate.bat  # On Windows

# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_data_validation.py

# Run with verbose output
python -m pytest tests/ -v
```

## Test Structure

- `test_data_validation.py`: Tests for the data validation module
- `test_visualization.py`: Tests for the visualization functions

## Adding New Tests

When adding new functionality, please also add corresponding tests. Follow these principles:

1. Each test should be independent and not rely on other tests
2. Use descriptive test names that explain what is being tested
3. Use appropriate assertions to verify expected behavior
4. Mock external dependencies where appropriate
5. Follow the existing test structure and naming conventions 