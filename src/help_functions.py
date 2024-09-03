import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns


ANIMAL_SPECIES = ['Oxen', 'Bulls', 'Cows', 'Female cattle', 'Cattle', 'Calves',
                  'Young cattle', 'Pigs', 'Sheep', 'Lambs', 'Horses', 'Goats']


def prepare_data(data):
    """
    Prepares the input DataFrame by performing various data cleaning and transformation tasks.

    Parameters:
    - data (DataFrame): The input DataFrame containing raw data.

    Returns:
    - data (DataFrame): A cleaned and transformed DataFrame ready for analysis.

    """
    data = data.rename(columns={'Unnamed: 0': 'State', 'Unnamed: 1': 'Year', 'Unnamed: 2': 'Month'})

    data = data.set_index(data.index - 3)

    data = data.dropna()

    data["Year"] = data["Year"].astype(int)

    data['State'] = data['State'].str.replace("ï¿½", "ü")

    data = rename_columns(data)

    data = data.replace({'-': pd.NA, 'x': pd.NA})

    data = calculate_totals_and_generate_columns(data)

    return data


def rename_columns(data):
    """
    Renames columns in a DataFrame based on a specified naming convention.

    Parameters:
    - data (DataFrame): The input DataFrame containing columns to be renamed.

    Returns:
    - DataFrame: A DataFrame with columns renamed according to the specified convention.
    """
    for species in ANIMAL_SPECIES:
        data = data.rename(columns={species: species + '_' + 'DoNr',
                                    species + ".1": species + '_' + 'DoT',
                                    species + ".2": species + '_' + 'FoNr',
                                    species + ".3": species + '_' + 'FoT',
                                    species + ".4": species + '_' + 'HoNr',
                                    species + ".5": species + '_' + 'HoT'})

    return data


def calculate_totals_and_generate_columns(data):
    """
    Calculates totals for domestic, foreign, and home and generates corresponding columns.

    Parameters:
    - data (DataFrame): The input DataFrame containing columns for domestic, foreign, and home data.

    Returns:
    - DataFrame: A DataFrame with additional columns for total domestic, foreign, and home data.

    """
    data['Total Domestic(Nr)'] = data.filter(regex='_DoNr').apply(pd.to_numeric, errors='coerce').sum(axis=1)
    data['Total Foreign(Nr)'] = data.filter(regex='_FoNr').apply(pd.to_numeric, errors='coerce').sum(axis=1)
    data['Total Home(Nr)'] = data.filter(regex='_HoNr').apply(pd.to_numeric, errors='coerce').sum(axis=1)

    data['Total Domestic(t)'] = data.filter(regex='_DoT').apply(pd.to_numeric, errors='coerce').sum(axis=1)
    data['Total Foreign(t)'] = data.filter(regex='_FoT').apply(pd.to_numeric, errors='coerce').sum(axis=1)
    data['Total Home(t)'] = data.filter(regex='_HoT').apply(pd.to_numeric, errors='coerce').sum(axis=1)

    return data


def line_plot_total_animals_slaughtered(data, time_range=None):
    """
    Generates a line plot showing the total number of slaughtered domestic animals over time.

    Parameters:
    - data (DataFrame): The input DataFrame containing data on slaughtered animals.
    - time_range (tuple, optional): A tuple specifying the range of years to include in the plot.
                                    If not provided, all years will be considered.

    Returns:
    - None

    """
    if time_range:
        data = data[(data['Year'] >= time_range[0]) & (data['Year'] <= time_range[1])]

    catalog_aggregated = data.groupby(['Year']).sum().reset_index()

    plt.figure(figsize=(20, 10))
    sns.lineplot(data=catalog_aggregated, x='Year', y='Total Domestic(Nr)', color="green")
    plt.title(f'Total number of domestic slaugthered animals over time from {time_range[0]} to {time_range[1]}')
    plt.ylabel('animal count')

    plt.fill_between(catalog_aggregated['Year'], catalog_aggregated['Total Domestic(Nr)'], color='lightgreen',
                     alpha=0.3)

    plt.yscale('log')
    plt.xlabel('year')
    plt.grid(True, axis="both")
    plt.show()


def bar_plot_most_slaugthered_animals(data, time_range=None):
    """
    Generates a bar plot showing the count of the most slaughtered animal species over time.

    Parameters:
    - data (DataFrame): The input DataFrame containing data on slaughtered animals.
    - time_range (tuple, optional): A tuple specifying the range of years to include in the plot.
                                    If not provided, all years will be considered.

    Returns:
    - None

    """
    if time_range:
        data = data[(data['Year'] >= time_range[0]) & (data['Year'] <= time_range[1])]

    species_counts = []
    for species in ANIMAL_SPECIES:
        species_counts.append(data[f"{species}_DoNr"].apply(pd.to_numeric, errors='coerce').sum())

    data = pd.DataFrame({'Species': ANIMAL_SPECIES, 'Count': species_counts})
    data = data.sort_values(by='Count', ascending=False)

    plt.figure(figsize=(20, 10))
    ax = sns.barplot(data=data, x='Species', y='Count', palette='Greens_r')
    plt.title(f'Most slaugthered animal species from {time_range[0]} to {time_range[1]}')
    plt.xlabel('animal species')
    plt.ylabel('animal count')
    plt.yscale('log')
    plt.xticks(rotation=90)

    ax.grid(True, axis='y')
    ax.set_axisbelow(True)

    plt.show()


def plot_total_animals_slaughtered_by_region(data, time_range=None):
    """
    Generates a line plot showing the total number of slaughtered domestic animals by region over time.

    Parameters:
    - data (DataFrame): The input DataFrame containing data on slaughtered animals by region.
    - time_range (tuple, optional): A tuple specifying the range of years to include in the plot.
                                    If not provided, all years will be considered.

    Returns:
    - None

    """
    if time_range:
        data = data[(data['Year'] >= time_range[0]) & (data['Year'] <= time_range[1])]

    data_aggregated = data.groupby(['State', 'Year']).sum().reset_index()

    data_aggregated = data_aggregated.sort_values(by=['Year', 'Total Domestic(Nr)'], ascending=[True, False])

    plt.figure(figsize=(20, 10))
    ax = sns.lineplot(data=data_aggregated, x='Year', y='Total Domestic(Nr)', hue='State', palette="Greens_r")
    plt.title(f'Total number of slaugthered animals by year and state from {time_range[0]} to {time_range[1]}')
    plt.xlabel('year')
    plt.ylabel('animal count')
    plt.xticks(rotation=90)

    ax.grid(True, axis='y')
    ax.set_axisbelow(True)

    plt.legend(title='Region', bbox_to_anchor=(1, 1), loc='upper left')
    plt.show()


def plot_seasonal_fluctuations(data, time_range=None):
    """
    Generates a line plot showing the average seasonal fluctuations of slaughtered animals
    over the specified time range.

    Parameters:
    - data (DataFrame): The input DataFrame containing data on slaughtered animals.
    - time_range (tuple, optional): A tuple specifying the range of years to include in the plot.
                                    If not provided, all years will be considered.

    Returns:
    - None

    """
    if time_range:
        data = data[(data['Year'] >= time_range[0]) & (data['Year'] <= time_range[1])]

    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                    'November', 'December']

    data['Month'] = pd.Categorical(data['Month'], categories=months_order, ordered=True)

    monthly_avg = data.groupby('Month')['Total Domestic(Nr)'].mean().reset_index()

    plt.figure(figsize=(20, 10))
    sns.lineplot(data=monthly_avg, x='Month', y='Total Domestic(Nr)', color="green")

    plt.fill_between(monthly_avg['Month'], monthly_avg['Total Domestic(Nr)'], 250000,
                     where=(monthly_avg['Total Domestic(Nr)'] >= 200000), color='lightgreen', alpha=0.3)

    plt.title(f'Average seasonal fluctuations of slaughtered animals from {time_range[0]} to {time_range[1]}')
    plt.xlabel('month')
    plt.ylabel('number of animals')
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def plot_slaughter_distribution(data, time_range=None):
    """
    Generates a bar plot showing the distribution of domestic slaughter and home slaughter by region
    over the specified time range.

    Parameters:
    - data (DataFrame): The input DataFrame containing data on slaughtered animals.
    - time_range (tuple, optional): A tuple specifying the range of years to include in the plot.
                                    If not provided, all years will be considered.

    Returns:
    - None

    """
    if time_range:
        data = data[(data['Year'] >= time_range[0]) & (data['Year'] <= time_range[1])]

    domestic_slaughter = data.groupby('State')['Total Domestic(Nr)'].sum().reset_index()
    home_slaughter = data.groupby('State')['Total Home(Nr)'].sum().reset_index()

    domestic_slaughter = domestic_slaughter.sort_values(by='Total Domestic(Nr)', ascending=False)
    home_slaughter = home_slaughter.reindex(domestic_slaughter.index)

    bar_width = 0.35

    states = domestic_slaughter['State'].unique()
    x = np.arange(len(states))

    plt.figure(figsize=(20, 10))

    plt.grid(True, axis='y')

    plt.bar(x - bar_width / 2, domestic_slaughter['Total Domestic(Nr)'], bar_width, color='green',
            label='Domestic slaugther')
    plt.bar(x + bar_width / 2, home_slaughter['Total Home(Nr)'], bar_width, color='lightgreen', label='Home slaugther')

    plt.title(
        f'Distribution of domestic slaugther and home slaugther by region from {time_range[0]} to {time_range[1]}')
    plt.xlabel('region')
    plt.ylabel('number of animals')
    plt.xticks(ticks=x, labels=states, rotation=90)
    plt.yscale('log')
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_slaughter_distribution_by_state_map(data, time_range=None):
    """
    Generates a choropleth map showing the distribution of slaughtered domestic animals by state
    over the specified time range.

    Parameters:
    - data (DataFrame): The input DataFrame containing data on slaughtered animals.
    - time_range (tuple, optional): A tuple specifying the range of years to include in the plot.
                                    If not provided, all years will be considered.

    Returns:
    - None

    """
    if time_range:
        data = data[(data['Year'] >= time_range[0]) & (data['Year'] <= time_range[1])]

    fp = "../data/geomap/vg2500_bld.shp"
    map_df = gpd.read_file(fp)

    grouped_catalog = data.groupby("State").sum().reset_index()

    merged = map_df.set_index("GEN").join(grouped_catalog.set_index("State"))

    fig, ax = plt.subplots(1, 1, figsize=(20, 10))

    merged.plot(column='Total Domestic(Nr)', cmap='Greens', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True,
                legend_kwds={'shrink': 0.5})

    ax.set_title(f'Total number of domestic slaugthered animals {time_range[0]} to {time_range[1]}')
    ax.axis('off')
    plt.show()


# function for testing
if __name__ == "__main__":
    catalog = pd.read_csv(
        "../data/animal_slaugther_ger.csv",
        header=4, sep=";", encoding="latin1", skipfooter=4)
    catalog = prepare_data(catalog)

    line_plot_total_animals_slaughtered(catalog, time_range=(1991, 2023))

    bar_plot_most_slaugthered_animals(catalog, time_range=(1991, 2023))

    plot_total_animals_slaughtered_by_region(catalog, time_range=(1991, 2023))

    plot_seasonal_fluctuations(catalog, time_range=(1991, 2023))

    plot_slaughter_distribution(catalog, time_range=(1991, 2023))

    plot_slaughter_distribution_by_state_map(catalog, time_range=(1991, 2023))
