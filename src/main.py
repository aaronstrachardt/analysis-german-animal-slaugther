#!/usr/bin/env python3
"""
Main script for the German animal slaughter analysis project.

This script demonstrates the use of the modular code structure to perform
analysis on the German animal slaughter dataset.
"""

import os
import sys
import pandas as pd
import argparse
from modules.config import DATA_PATH, DEFAULT_TIME_RANGE
from modules.data_preparation import load_data, prepare_data
from modules.data_validation import validate_dataframe, get_data_summary
from modules.visualization import (
    plot_total_animals_slaughtered,
    plot_most_slaughtered_animals,
    plot_animals_by_region,
    plot_seasonal_fluctuations,
    plot_slaughter_distribution
)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Analysis of German animal slaughter data"
    )
    parser.add_argument(
        "--data-path",
        default=DATA_PATH,
        help="Path to the CSV file containing the data"
    )
    parser.add_argument(
        "--start-year",
        type=int,
        default=DEFAULT_TIME_RANGE[0],
        help="Start year for the analysis"
    )
    parser.add_argument(
        "--end-year",
        type=int,
        default=DEFAULT_TIME_RANGE[1],
        help="End year for the analysis"
    )
    parser.add_argument(
        "--output-dir",
        default="./output",
        help="Directory to save the output files"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate the data without generating plots"
    )
    
    return parser.parse_args()


def main():
    """Run the main analysis workflow."""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    print(f"Loading data from {args.data_path}...")
    try:
        # Load and prepare data
        raw_data = load_data(args.data_path)
        print("Preparing data...")
        data = prepare_data(raw_data)
        
        # Validate data
        print("Validating data...")
        validation_results = validate_dataframe(data)
        
        if not validation_results['valid']:
            print("Warning: Data validation issues detected:")
            for error in validation_results['errors']:
                print(f"  - {error}")
            
            user_input = input("Continue with analysis anyway? (y/n): ")
            if user_input.lower() != 'y':
                print("Analysis aborted.")
                return
        
        # Get data summary
        summary = get_data_summary(data)
        print("\nData Summary:")
        print(f"  - Shape: {summary['shape']}")
        print(f"  - Years range: {summary['years_range']}")
        print(f"  - Number of states: {len(summary['states'])}")
        if 'total_domestic_animals' in summary:
            print(f"  - Total domestic animals: {summary['total_domestic_animals']:,}")
        if 'total_foreign_animals' in summary:
            print(f"  - Total foreign animals: {summary['total_foreign_animals']:,}")
        if 'total_home_animals' in summary:
            print(f"  - Total home animals: {summary['total_home_animals']:,}")
        
        # If --validate-only flag is set, stop here
        if args.validate_only:
            print("Validation completed. Skipping plot generation.")
            return
        
        # Set time range for analysis
        time_range = (args.start_year, args.end_year)
        print(f"\nGenerating plots for time range: {time_range[0]} to {time_range[1]}...")
        
        # Generate and save plots
        print("1. Generating total animals slaughtered plot...")
        fig1 = plot_total_animals_slaughtered(data, time_range)
        fig1.write_html(os.path.join(args.output_dir, "total_animals_slaughtered.html"))
        fig1.write_image(os.path.join(args.output_dir, "total_animals_slaughtered.png"))
        
        print("2. Generating most slaughtered animals plot...")
        fig2 = plot_most_slaughtered_animals(data, time_range)
        fig2.write_html(os.path.join(args.output_dir, "most_slaughtered_animals.html"))
        fig2.write_image(os.path.join(args.output_dir, "most_slaughtered_animals.png"))
        
        print("3. Generating animals by region plot...")
        fig3 = plot_animals_by_region(data, time_range)
        fig3.write_html(os.path.join(args.output_dir, "animals_by_region.html"))
        fig3.write_image(os.path.join(args.output_dir, "animals_by_region.png"))
        
        print("4. Generating seasonal fluctuations plot...")
        fig4 = plot_seasonal_fluctuations(data, time_range)
        fig4.write_html(os.path.join(args.output_dir, "seasonal_fluctuations.html"))
        fig4.write_image(os.path.join(args.output_dir, "seasonal_fluctuations.png"))
        
        print("5. Generating slaughter distribution plot...")
        fig5 = plot_slaughter_distribution(data, time_range)
        fig5.write_html(os.path.join(args.output_dir, "slaughter_distribution.html"))
        fig5.write_image(os.path.join(args.output_dir, "slaughter_distribution.png"))
        
        print(f"\nAnalysis completed. Results saved to {args.output_dir}/")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 