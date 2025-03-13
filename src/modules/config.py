"""
Configuration module for the German animal slaughter analysis project.

This module contains constants, settings, and configuration values used throughout the project.
"""

# Animal species included in the analysis
ANIMAL_SPECIES = [
    'Oxen', 'Bulls', 'Cows', 'Female cattle', 'Cattle', 'Calves',
    'Young cattle', 'Pigs', 'Sheep', 'Lambs', 'Horses', 'Goats'
]

# Slaughter types and their abbreviations
SLAUGHTER_TYPES = {
    'Do': 'Domestic slaughter',
    'Fo': 'Foreign slaughter',
    'Ho': 'Home slaughter'
}

# Measurement types and their abbreviations
MEASUREMENT_TYPES = {
    'Nr': 'Animal count',
    'T': 'Quantity in tons'
}

# Default time range for analysis if not specified
DEFAULT_TIME_RANGE = (1991, 2023)

# Default plot settings
PLOT_FIGSIZE = (20, 10)
PLOT_PALETTE = 'Greens_r'
PLOT_COLOR = 'green'
PLOT_LIGHT_COLOR = 'lightgreen'

# Month ordering for seasonal analysis
MONTHS_ORDER = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# File paths
GEOMAP_PATH = "./data/geomap/vg2500_bld.shp"
DATA_PATH = "./data/animal_slaugther_ger.csv"
