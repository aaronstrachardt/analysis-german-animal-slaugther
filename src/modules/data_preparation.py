"""
Data preparation module for the German animal slaughter analysis project.

This module provides functions for loading, cleaning, and transforming
the German animal slaughter dataset.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
from .config import ANIMAL_SPECIES


def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads the animal slaughter data from a CSV file.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file containing the data
        
    Returns:
    --------
    pd.DataFrame
        The loaded dataset as a pandas DataFrame
        
    Notes:
    ------
    The CSV file is expected to have a specific format with header rows.
    The first 4 rows contain metadata and are skipped during loading.
    The function handles encoding issues with Latin-1 encoding.
    """
    try:
        data = pd.read_csv(
            file_path,
            header=4,
            sep=";",
            encoding="latin1",
            skipfooter=4,
            engine="python"
        )
        return data
    except Exception as e:
        print(f"Error loading data from {file_path}: {str(e)}")
        raise


def rename_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Renames columns in a DataFrame based on the animal species naming convention.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The input DataFrame containing columns to be renamed
        
    Returns:
    --------
    pd.DataFrame
        A DataFrame with columns renamed according to the specified convention:
        
        The naming convention used is:
        - {species}_DoNr: Domestic slaughter, animal count
        - {species}_DoT: Domestic slaughter, quantity in tons
        - {species}_FoNr: Foreign slaughter, animal count
        - {species}_FoT: Foreign slaughter, quantity in tons
        - {species}_HoNr: Home slaughter, animal count
        - {species}_HoT: Home slaughter, quantity in tons
    """
    for species in ANIMAL_SPECIES:
        data = data.rename(columns={
            species: species + '_' + 'DoNr',
            species + ".1": species + '_' + 'DoT',
            species + ".2": species + '_' + 'FoNr',
            species + ".3": species + '_' + 'FoT',
            species + ".4": species + '_' + 'HoNr',
            species + ".5": species + '_' + 'HoT'
        })
    
    return data


def calculate_totals(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates totals for domestic, foreign, and home slaughter data and adds them as new columns.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The input DataFrame containing columns for domestic, foreign, and home data
        
    Returns:
    --------
    pd.DataFrame
        A DataFrame with additional columns for total domestic, foreign, and home data.
        New columns added:
        - Total Domestic(Nr): Total number of domestically slaughtered animals
        - Total Foreign(Nr): Total number of foreign slaughtered animals
        - Total Home(Nr): Total number of home slaughtered animals
        - Total Domestic(t): Total weight of domestically slaughtered animals in tons
        - Total Foreign(t): Total weight of foreign slaughtered animals in tons
        - Total Home(t): Total weight of home slaughtered animals in tons
    """
    # Calculate totals for animal counts (Nr)
    data['Total Domestic(Nr)'] = data.filter(regex='_DoNr').apply(pd.to_numeric, errors='coerce').sum(axis=1)
    data['Total Foreign(Nr)'] = data.filter(regex='_FoNr').apply(pd.to_numeric, errors='coerce').sum(axis=1)
    data['Total Home(Nr)'] = data.filter(regex='_HoNr').apply(pd.to_numeric, errors='coerce').sum(axis=1)
    
    # Calculate totals for weights (t)
    data['Total Domestic(t)'] = data.filter(regex='_DoT').apply(pd.to_numeric, errors='coerce').sum(axis=1)
    data['Total Foreign(t)'] = data.filter(regex='_FoT').apply(pd.to_numeric, errors='coerce').sum(axis=1)
    data['Total Home(t)'] = data.filter(regex='_HoT').apply(pd.to_numeric, errors='coerce').sum(axis=1)
    
    return data


def prepare_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares the input DataFrame by performing various data cleaning and transformation tasks.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The input DataFrame containing raw data
        
    Returns:
    --------
    pd.DataFrame
        A cleaned and transformed DataFrame ready for analysis
        
    Notes:
    ------
    This function performs the following operations:
    1. Renames unnamed columns to 'State', 'Year', and 'Month'
    2. Adjusts the DataFrame index
    3. Drops rows with NaN values in key columns
    4. Converts the 'Year' column to integer type
    5. Fixes encoding issues in the 'State' column
    6. Renames animal species columns using a standardized convention
    7. Replaces special characters ('-', 'x') with NaN values
    8. Calculates total columns for domestic, foreign, and home slaughter data
    """
    # Rename unnamed columns
    data = data.rename(columns={'Unnamed: 0': 'State', 'Unnamed: 1': 'Year', 'Unnamed: 2': 'Month'})
    
    # Adjust index (to account for header rows)
    data = data.set_index(data.index - 3)
    
    # Drop rows with NaN values in key columns
    data = data.dropna(subset=['State', 'Year', 'Month'])
    
    # Convert Year to integer
    data["Year"] = data["Year"].astype(int)
    
    # Fix encoding issues
    data['State'] = data['State'].str.replace("ï¿½", "ü")
    
    # Rename columns using standardized convention
    data = rename_columns(data)
    
    # Replace special characters with NaN
    data = data.replace({'-': pd.NA, 'x': pd.NA})
    
    # Calculate totals
    data = calculate_totals(data)
    
    return data
