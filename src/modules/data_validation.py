"""
Data validation module for the German animal slaughter analysis project.

This module provides functions for validating, cleaning, and verifying
the integrity of the input data before analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from .config import ANIMAL_SPECIES


def validate_columns(data: pd.DataFrame) -> List[str]:
    """
    Validates that the DataFrame has the required columns.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame to validate
        
    Returns:
    --------
    List[str]
        A list of missing columns if any, otherwise an empty list
    """
    required_columns = ['State', 'Year', 'Month']
    missing_columns = [col for col in required_columns if col not in data.columns]
    return missing_columns


def validate_animal_species_columns(data: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validates that all animal species columns exist in some form.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame to validate
        
    Returns:
    --------
    Tuple[bool, List[str]]
        A tuple containing a boolean indicating if all species were found and 
        a list of missing species
    """
    found_species = []
    for species in ANIMAL_SPECIES:
        if any(species in col for col in data.columns):
            found_species.append(species)
    
    missing_species = [species for species in ANIMAL_SPECIES if species not in found_species]
    return len(missing_species) == 0, missing_species


def validate_dataframe(data: pd.DataFrame) -> Dict[str, Union[bool, List[str]]]:
    """
    Performs comprehensive validation on the input DataFrame.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame to validate
    
    Returns:
    --------
    Dict[str, Union[bool, List[str]]]
        A dictionary containing validation results with the following keys:
        - 'valid': Boolean indicating if the DataFrame passed all validations
        - 'missing_columns': List of missing required columns
        - 'missing_species': List of missing animal species
        - 'null_percentage': Percentage of null values in the DataFrame
        - 'errors': List of validation error messages
    """
    results = {
        'valid': True,
        'missing_columns': [],
        'missing_species': [],
        'null_percentage': 0.0,
        'errors': []
    }
    
    # Check for required columns
    missing_columns = validate_columns(data)
    if missing_columns:
        results['valid'] = False
        results['missing_columns'] = missing_columns
        results['errors'].append(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Check for animal species columns
    species_valid, missing_species = validate_animal_species_columns(data)
    if not species_valid:
        results['valid'] = False
        results['missing_species'] = missing_species
        results['errors'].append(f"Missing animal species columns: {', '.join(missing_species)}")
    
    # Check for null values
    null_count = data.isnull().sum().sum()
    total_values = data.size
    null_percentage = (null_count / total_values) * 100 if total_values > 0 else 0
    results['null_percentage'] = null_percentage
    
    if null_percentage > 50:  # Consider it a problem if more than 50% values are null
        results['valid'] = False
        results['errors'].append(f"High percentage of null values: {null_percentage:.2f}%")
    
    # Validate data types
    if 'Year' in data.columns:
        if not pd.api.types.is_numeric_dtype(data['Year']):
            results['valid'] = False
            results['errors'].append("Year column is not numeric")
    
    # Check for duplicate rows
    if data.duplicated().any():
        results['valid'] = False
        results['errors'].append(f"Found {data.duplicated().sum()} duplicate rows")
    
    return results


def get_data_summary(data: pd.DataFrame) -> Dict[str, any]:
    """
    Generates a summary of the dataset.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame to summarize
    
    Returns:
    --------
    Dict[str, any]
        A dictionary containing summary statistics and information about the dataset:
        - 'shape': Tuple of (rows, columns)
        - 'years_range': Tuple of (min_year, max_year)
        - 'states': List of unique states
        - 'months': List of unique months
        - 'total_animals': Total number of animals in the dataset
        - 'basic_stats': Basic statistics for numeric columns
    """
    summary = {
        'shape': data.shape,
        'years_range': (data['Year'].min(), data['Year'].max()) if 'Year' in data.columns else None,
        'states': data['State'].unique().tolist() if 'State' in data.columns else None,
        'months': data['Month'].unique().tolist() if 'Month' in data.columns else None
    }
    
    # Calculate total animals if the total columns exist
    if 'Total Domestic(Nr)' in data.columns:
        summary['total_domestic_animals'] = data['Total Domestic(Nr)'].sum()
    if 'Total Foreign(Nr)' in data.columns:
        summary['total_foreign_animals'] = data['Total Foreign(Nr)'].sum()
    if 'Total Home(Nr)' in data.columns:
        summary['total_home_animals'] = data['Total Home(Nr)'].sum()
    
    # Get basic stats for the main numeric columns
    numeric_columns = ['Total Domestic(Nr)', 'Total Foreign(Nr)', 'Total Home(Nr)']
    numeric_columns = [col for col in numeric_columns if col in data.columns]
    if numeric_columns:
        summary['basic_stats'] = data[numeric_columns].describe().to_dict()
    
    return summary
