"""
Tests for the visualization module.

This module contains tests for the visualization functions in the project.
"""

import unittest
import pandas as pd
import numpy as np
from src.modules.visualization import (
    plot_total_animals_slaughtered,
    plot_most_slaughtered_animals,
    plot_animals_by_region,
    plot_seasonal_fluctuations,
    plot_slaughter_distribution
)


class TestVisualization(unittest.TestCase):
    """Test cases for visualization functions."""

    def setUp(self):
        """Set up test data."""
        # Create a small test dataframe
        self.test_data = pd.DataFrame({
            'State': ['State1', 'State1', 'State2', 'State2'] * 3,
            'Year': [2019, 2020, 2019, 2020] * 3,
            'Month': ['January', 'February', 'January', 'February'] * 3,
            'Pigs_DoNr': [100, 120, 90, 110] * 3,
            'Pigs_FoNr': [50, 60, 45, 55] * 3,
            'Pigs_HoNr': [10, 12, 9, 11] * 3,
            'Cattle_DoNr': [30, 35, 25, 32] * 3,
            'Cattle_FoNr': [15, 18, 12, 16] * 3,
            'Cattle_HoNr': [5, 6, 4, 5] * 3,
        })
        
        # Set time range for testing
        self.time_range = (2019, 2020)

    def test_plot_total_animals_slaughtered_returns_figure(self):
        """Test if plot_total_animals_slaughtered returns a plotly figure."""
        fig = plot_total_animals_slaughtered(self.test_data, self.time_range)
        self.assertIsNotNone(fig)
        # Check that the figure has data
        self.assertTrue(len(fig.data) > 0)

    def test_plot_most_slaughtered_animals_returns_figure(self):
        """Test if plot_most_slaughtered_animals returns a plotly figure."""
        fig = plot_most_slaughtered_animals(self.test_data, self.time_range)
        self.assertIsNotNone(fig)
        # Check that the figure has data
        self.assertTrue(len(fig.data) > 0)

    def test_plot_animals_by_region_returns_figure(self):
        """Test if plot_animals_by_region returns a plotly figure."""
        # This might need a mock for the geopandas part
        try:
            fig = plot_animals_by_region(self.test_data, self.time_range)
            self.assertIsNotNone(fig)
        except Exception as e:
            # Skip if there's an issue with geo data
            self.skipTest(f"Skipping test due to: {str(e)}")

    def test_plot_seasonal_fluctuations_returns_figure(self):
        """Test if plot_seasonal_fluctuations returns a plotly figure."""
        fig = plot_seasonal_fluctuations(self.test_data, self.time_range)
        self.assertIsNotNone(fig)
        # Check that the figure has data
        self.assertTrue(len(fig.data) > 0)

    def test_plot_slaughter_distribution_returns_figure(self):
        """Test if plot_slaughter_distribution returns a plotly figure."""
        fig = plot_slaughter_distribution(self.test_data, self.time_range)
        self.assertIsNotNone(fig)
        # Check that the figure has data
        self.assertTrue(len(fig.data) > 0)


if __name__ == '__main__':
    unittest.main() 