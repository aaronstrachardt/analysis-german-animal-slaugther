# Contributing to Analysis of German Animal Slaughter

Thank you for your interest in contributing to the "Analysis of German Animal Slaughter" project! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Contact](#contact)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [strachardt1@uni-potsdam.de](mailto:strachardt1@uni-potsdam.de).

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** to your local machine:
   ```bash
   git clone https://github.com/YOUR-USERNAME/analysis-german-animal-slaughter.git
   cd analysis-german-animal-slaughter
   ```
3. **Set up the development environment**:
   ```bash
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

## Project Structure

The repository is organized as follows:

```
analysis-german-animal-slaughter/
├── data/                  # Dataset files
│   ├── animal_slaugther_ger.csv  # Main dataset
│   └── geomap/            # Geospatial data for mapping
├── docs/                  # Documentation files
├── src/                   # Source code
│   ├── modules/           # Python modules
│   │   ├── __init__.py    # Package initialization
│   │   ├── config.py      # Configuration parameters
│   │   ├── data_preparation.py  # Data loading and cleaning
│   │   ├── data_validation.py   # Data validation
│   │   └── visualization.py     # Visualization functions
│   ├── main.py            # Command-line interface
│   └── main.ipynb         # Jupyter notebook with analysis
├── tests/                 # Test files
│   ├── __init__.py
│   └── test_*.py          # Unit tests
├── .gitignore             # Git ignore file
├── CITATION.cff           # Citation information
├── CONTRIBUTING.md        # This file
├── LICENSE.md             # License information
├── README.md              # Project overview
└── requirements.txt       # Required Python packages
```

## Development Workflow

1. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit them with clear, descriptive commit messages:
   ```bash
   git add .
   git commit -m "Add feature X" -m "This implements feature X which does Y and Z."
   ```

3. **Run tests** to ensure your changes don't break existing functionality:
   ```bash
   pytest
   ```

4. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a pull request** from your fork to the main repository.

## Coding Standards

We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code. Additionally:

- Use [type hints](https://docs.python.org/3/library/typing.html) for function parameters and return values.
- Write comprehensive docstrings using the [NumPy style](https://numpydoc.readthedocs.io/en/latest/format.html).
- Keep functions focused on a single responsibility.
- Use meaningful variable and function names.

We use the following tools to ensure code quality:
- [Black](https://black.readthedocs.io/) for code formatting
- [mypy](http://mypy-lang.org/) for static type checking
- [pytest](https://docs.pytest.org/) for testing

You can run these tools using the following commands:
```bash
# Format code
black src/ tests/

# Type checking
mypy src/ tests/

# Run tests
pytest
```

## Testing

We use [pytest](https://docs.pytest.org/) for testing. All new features should include tests. Tests should be placed in the `tests/` directory with a file name that matches the module being tested (e.g., `test_data_validation.py` for `data_validation.py`).

To run tests:
```bash
pytest
```

## Documentation

Documentation is crucial for this project. Please follow these guidelines:

- All functions, classes, and modules should have docstrings.
- Use NumPy-style docstrings with sections for Parameters, Returns, Examples, etc.
- Update the README.md if your changes impact the project overview or usage.
- Consider updating or adding to the example Jupyter notebook if relevant.

## Pull Request Process

1. Ensure your code follows our coding standards and passes all tests.
2. Update documentation as needed.
3. Submit your pull request with a clear title and description.
4. Link any relevant issues in your pull request description.
5. Be responsive to feedback and be prepared to make additional changes if requested.

## Contact

If you have questions or need help, you can:
- Open an issue on GitHub
- Contact the maintainer: [strachardt1@uni-potsdam.de](mailto:strachardt1@uni-potsdam.de)

Thank you for contributing to the Analysis of German Animal Slaughter project! 