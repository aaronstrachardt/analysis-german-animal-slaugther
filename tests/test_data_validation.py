"""
Tests for the data validation module.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modules.data_validation import (
    validate_columns,
    validate_animal_species_columns,
    validate_dataframe,
    get_data_summary
)
from src.modules.config import ANIMAL_SPECIES


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'State': ['Bayern', 'Berlin', 'Hamburg'],
        'Year': [2000, 2001, 2002],
        'Month': ['January', 'February', 'March'],
        'Oxen_DoNr': [100, 200, 300],
        'Oxen_DoT': [10, 20, 30],
        'Bulls_DoNr': [400, 500, 600],
        'Total Domestic(Nr)': [500, 700, 900],
        'Total Home(Nr)': [50, 70, 90],
    })


@pytest.fixture
def invalid_dataframe():
    """Create an invalid DataFrame for testing."""
    return pd.DataFrame({
        'State': ['Bayern', 'Berlin', 'Hamburg'],
        # Missing Year column
        'Month': ['January', 'February', 'March'],
        # Missing animal species columns
    })


def test_validate_columns_valid(sample_dataframe):
    """Test validate_columns with a valid DataFrame."""
    missing_columns = validate_columns(sample_dataframe)
    assert len(missing_columns) == 0


def test_validate_columns_invalid(invalid_dataframe):
    """Test validate_columns with an invalid DataFrame."""
    missing_columns = validate_columns(invalid_dataframe)
    assert 'Year' in missing_columns


def test_validate_animal_species_columns_valid(sample_dataframe):
    """Test validate_animal_species_columns with a valid DataFrame."""
    is_valid, missing_species = validate_animal_species_columns(sample_dataframe)
    assert not is_valid  # It's not fully valid because we only have 2 animal species
    assert 'Cows' in missing_species
    assert 'Oxen' not in missing_species  # We have Oxen in the DataFrame
    assert 'Bulls' not in missing_species  # We have Bulls in the DataFrame


def test_validate_animal_species_columns_invalid(invalid_dataframe):
    """Test validate_animal_species_columns with an invalid DataFrame."""
    is_valid, missing_species = validate_animal_species_columns(invalid_dataframe)
    assert not is_valid
    assert len(missing_species) == len(ANIMAL_SPECIES)  # All species should be missing


def test_validate_dataframe_valid(sample_dataframe):
    """Test validate_dataframe with a valid DataFrame."""
    results = validate_dataframe(sample_dataframe)
    assert results['valid'] is False  # Not fully valid because we don't have all animal species
    assert len(results['missing_columns']) == 0
    assert len(results['missing_species']) > 0
    assert results['null_percentage'] == 0.0


def test_validate_dataframe_invalid(invalid_dataframe):
    """Test validate_dataframe with an invalid DataFrame."""
    results = validate_dataframe(invalid_dataframe)
    assert results['valid'] is False
    assert 'Year' in results['missing_columns']
    assert len(results['missing_species']) == len(ANIMAL_SPECIES)
    assert len(results['errors']) >= 2  # At least 2 errors (missing columns and species)


def test_get_data_summary(sample_dataframe):
    """Test get_data_summary."""
    summary = get_data_summary(sample_dataframe)
    assert summary['shape'] == (3, 8)
    assert summary['years_range'] == (2000, 2002)
    assert len(summary['states']) == 3
    assert 'Bayern' in summary['states']
    assert summary['total_domestic_animals'] == 2100 