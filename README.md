# German Animal Slaughter Analysis

This repository contains a comprehensive data analysis toolkit for examining animal slaughter statistics in Germany. It provides tools for data preparation, validation, analysis, and visualization to help understand patterns and trends in animal slaughter across different regions of Germany.

## Overview

This project analyzes German animal slaughter data with a focus on:
- Total number of animals slaughtered over time
- Most commonly slaughtered animal types
- Regional distribution of animal slaughter
- Seasonal fluctuations in slaughter rates
- Distribution patterns across the country

## Features

- Data loading and preprocessing pipeline
- Data validation to ensure data quality
- Multiple visualization options:
  - Time series analysis of total slaughters
  - Comparative analysis by animal type
  - Geographical distribution by region
  - Seasonal trend analysis
  - Statistical distribution visualizations
- Command-line interface for customizable analysis

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/analysis-german-animal-slaugther.git
   cd analysis-german-animal-slaugther
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

Run the main analysis script:

```
python src/main.py
```

Command line options:
```
python src/main.py --data-path data/animal_slaugther_ger.csv --output-dir output --start-year 2015 --end-year 2022
```

Parameters:
- `--data-path`: Path to the input data file (default: data/animal_slaugther_ger.csv)
- `--output-dir`: Directory for saving output files (default: output)
- `--start-year`: Start year for analysis
- `--end-year`: End year for analysis
- `--validate-only`: Only validate the data, skip plotting

### Jupyter Notebook

For interactive analysis, you can use the provided Jupyter notebook:

```
jupyter notebook src/main.ipynb
```

## Data

The repository includes a dataset (`data/animal_slaugther_ger.csv`) containing animal slaughter statistics for different regions of Germany. The data includes:
- Temporal information (year, month)
- Regional information (state/Bundesland)
- Animal types
- Slaughter counts

## Output

The analysis generates both HTML and PNG visualizations in the output directory, including:
- Total animals slaughtered over time
- Most slaughtered animal types
- Animals slaughtered by region
- Seasonal fluctuation patterns
- Slaughter distribution analysis

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the terms specified in [LICENSE.md](LICENSE.md).

## Citation

If you use this analysis in your research, please cite this repository according to the information in [CITATION.cff](CITATION.cff).
