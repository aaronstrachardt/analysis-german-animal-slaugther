"""
Visualization module for the German animal slaughter analysis project.

This module provides functions for creating interactive visualizations
of the German animal slaughter data using Plotly.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional, Union
import geopandas as gpd

from .config import (
    ANIMAL_SPECIES, 
    PLOT_FIGSIZE, 
    PLOT_COLOR, 
    PLOT_LIGHT_COLOR,
    PLOT_PALETTE,
    MONTHS_ORDER,
    GEOMAP_PATH,
    DEFAULT_TIME_RANGE
)


def plot_total_animals_slaughtered(
    data: pd.DataFrame, 
    time_range: Optional[Tuple[int, int]] = None,
    interactive: bool = True
) -> go.Figure:
    """
    Generates a line plot showing the total number of slaughtered domestic animals over time.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The input DataFrame containing data on slaughtered animals
    time_range : Tuple[int, int], optional
        A tuple specifying the range of years to include in the plot (start_year, end_year)
    interactive : bool, default=True
        Whether to create an interactive Plotly visualization
        
    Returns:
    --------
    plotly.graph_objects.Figure
        A Plotly figure object containing the visualization
    """
    # Filter by time range if specified
    if time_range:
        data = data[(data['Year'] >= time_range[0]) & (data['Year'] <= time_range[1])]
    else:
        time_range = DEFAULT_TIME_RANGE
    
    # Aggregate data by year
    catalog_aggregated = data.groupby(['Year']).sum().reset_index()
    
    # Create interactive Plotly figure
    fig = go.Figure()
    
    # Add trace for total domestic animals
    fig.add_trace(
        go.Scatter(
            x=catalog_aggregated['Year'],
            y=catalog_aggregated['Total Domestic(Nr)'],
            mode='lines',
            name='Total Domestic Animals',
            line=dict(color=PLOT_COLOR, width=2),
            fill='tozeroy',
            fillcolor=f'rgba(0, 128, 0, 0.2)'  # Light green with transparency
        )
    )
    
    # Update layout
    fig.update_layout(
        title=f'Total Number of Domestic Slaughtered Animals ({time_range[0]} to {time_range[1]})',
        xaxis_title='Year',
        yaxis_title='Animal Count',
        yaxis_type='log',
        template='plotly_white',
        width=PLOT_FIGSIZE[0] * 50,  # Convert from inches to pixels
        height=PLOT_FIGSIZE[1] * 50,
        hovermode='x unified'
    )
    
    # Add grid lines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig


def plot_most_slaughtered_animals(
    data: pd.DataFrame, 
    time_range: Optional[Tuple[int, int]] = None,
    interactive: bool = True
) -> go.Figure:
    """
    Generates a bar plot showing the count of the most slaughtered animal species over time.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The input DataFrame containing data on slaughtered animals
    time_range : Tuple[int, int], optional
        A tuple specifying the range of years to include in the plot (start_year, end_year)
    interactive : bool, default=True
        Whether to create an interactive Plotly visualization
        
    Returns:
    --------
    plotly.graph_objects.Figure
        A Plotly figure object containing the visualization
    """
    # Filter by time range if specified
    if time_range:
        data = data[(data['Year'] >= time_range[0]) & (data['Year'] <= time_range[1])]
    else:
        time_range = DEFAULT_TIME_RANGE
    
    # Calculate counts for each species
    species_counts = []
    for species in ANIMAL_SPECIES:
        species_counts.append(data[f"{species}_DoNr"].apply(pd.to_numeric, errors='coerce').sum())
    
    # Create DataFrame for plotting
    plot_data = pd.DataFrame({'Species': ANIMAL_SPECIES, 'Count': species_counts})
    plot_data = plot_data.sort_values(by='Count', ascending=False)
    
    # Create color gradient based on count values
    max_count = plot_data['Count'].max()
    normalized_counts = plot_data['Count'] / max_count
    colors = [f'rgba(0, 128, 0, {0.2 + 0.8 * val})' for val in normalized_counts]
    
    # Create interactive Plotly figure
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(
        go.Bar(
            x=plot_data['Species'],
            y=plot_data['Count'],
            marker_color=colors,
            text=plot_data['Count'].apply(lambda x: f'{x:,}'),
            textposition='auto'
        )
    )
    
    # Update layout
    fig.update_layout(
        title=f'Most Slaughtered Animal Species ({time_range[0]} to {time_range[1]})',
        xaxis_title='Animal Species',
        yaxis_title='Animal Count',
        yaxis_type='log',
        template='plotly_white',
        width=PLOT_FIGSIZE[0] * 50,  # Convert from inches to pixels
        height=PLOT_FIGSIZE[1] * 50,
    )
    
    # Update axes
    fig.update_xaxes(categoryorder='total descending')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig


def plot_animals_by_region(
    data: pd.DataFrame, 
    time_range: Optional[Tuple[int, int]] = None,
    interactive: bool = True
) -> go.Figure:
    """
    Generates a line plot showing the total number of slaughtered domestic animals by region over time.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The input DataFrame containing data on slaughtered animals by region
    time_range : Tuple[int, int], optional
        A tuple specifying the range of years to include in the plot (start_year, end_year)
    interactive : bool, default=True
        Whether to create an interactive Plotly visualization
        
    Returns:
    --------
    plotly.graph_objects.Figure
        A Plotly figure object containing the visualization
    """
    # Filter by time range if specified
    if time_range:
        data = data[(data['Year'] >= time_range[0]) & (data['Year'] <= time_range[1])]
    else:
        time_range = DEFAULT_TIME_RANGE
    
    # Aggregate data by state and year
    data_aggregated = data.groupby(['State', 'Year']).sum().reset_index()
    
    # Create interactive Plotly figure
    fig = px.line(
        data_aggregated,
        x='Year',
        y='Total Domestic(Nr)',
        color='State',
        title=f'Total Slaughtered Animals by Region ({time_range[0]} to {time_range[1]})',
        labels={'Total Domestic(Nr)': 'Animal Count', 'Year': 'Year'},
        log_y=True,
        width=PLOT_FIGSIZE[0] * 50,  # Convert from inches to pixels
        height=PLOT_FIGSIZE[1] * 50,
    )
    
    # Update layout
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            title='Region',
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='right',
            x=1
        )
    )
    
    # Update grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig


def plot_seasonal_fluctuations(
    data: pd.DataFrame, 
    time_range: Optional[Tuple[int, int]] = None,
    interactive: bool = True
) -> go.Figure:
    """
    Generates a line plot showing the average seasonal fluctuations of slaughtered animals
    over the specified time range.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The input DataFrame containing data on slaughtered animals
    time_range : Tuple[int, int], optional
        A tuple specifying the range of years to include in the plot (start_year, end_year)
    interactive : bool, default=True
        Whether to create an interactive Plotly visualization
        
    Returns:
    --------
    plotly.graph_objects.Figure
        A Plotly figure object containing the visualization
    """
    # Filter by time range if specified
    if time_range:
        data = data[(data['Year'] >= time_range[0]) & (data['Year'] <= time_range[1])]
    else:
        time_range = DEFAULT_TIME_RANGE
    
    # Convert Month to categorical for proper ordering
    data['Month'] = pd.Categorical(data['Month'], categories=MONTHS_ORDER, ordered=True)
    
    # Calculate monthly averages
    monthly_avg = data.groupby('Month')['Total Domestic(Nr)'].mean().reset_index()
    
    # Create interactive Plotly figure
    fig = go.Figure()
    
    # Add trace for monthly averages
    fig.add_trace(
        go.Scatter(
            x=monthly_avg['Month'],
            y=monthly_avg['Total Domestic(Nr)'],
            mode='lines+markers',
            name='Monthly Average',
            line=dict(color=PLOT_COLOR, width=2),
            marker=dict(size=8, color=PLOT_COLOR),
        )
    )
    
    # Highlight months above a certain threshold
    threshold = 200000
    highlight_months = monthly_avg[monthly_avg['Total Domestic(Nr)'] >= threshold]
    
    if not highlight_months.empty:
        fig.add_trace(
            go.Scatter(
                x=highlight_months['Month'],
                y=highlight_months['Total Domestic(Nr)'],
                mode='markers',
                name='Months Above Average',
                marker=dict(size=12, color='darkgreen'),
                showlegend=False
            )
        )
    
    # Update layout
    fig.update_layout(
        title=f'Average Seasonal Fluctuations in Animal Slaughter ({time_range[0]} to {time_range[1]})',
        xaxis_title='Month',
        yaxis_title='Average Animal Count',
        template='plotly_white',
        width=PLOT_FIGSIZE[0] * 50,  # Convert from inches to pixels
        height=PLOT_FIGSIZE[1] * 50,
        hovermode='x unified'
    )
    
    # Update grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig


def plot_slaughter_distribution(
    data: pd.DataFrame, 
    time_range: Optional[Tuple[int, int]] = None,
    interactive: bool = True
) -> go.Figure:
    """
    Generates a grouped bar plot showing the distribution of domestic slaughter and home slaughter
    by region over the specified time range.
    
    Parameters:
    -----------
    data : pd.DataFrame
        The input DataFrame containing data on slaughtered animals
    time_range : Tuple[int, int], optional
        A tuple specifying the range of years to include in the plot (start_year, end_year)
    interactive : bool, default=True
        Whether to create an interactive Plotly visualization
        
    Returns:
    --------
    plotly.graph_objects.Figure
        A Plotly figure object containing the visualization
    """
    # Filter by time range if specified
    if time_range:
        data = data[(data['Year'] >= time_range[0]) & (data['Year'] <= time_range[1])]
    else:
        time_range = DEFAULT_TIME_RANGE
    
    # Calculate sums by state
    domestic_slaughter = data.groupby('State')['Total Domestic(Nr)'].sum().reset_index()
    home_slaughter = data.groupby('State')['Total Home(Nr)'].sum().reset_index()
    
    # Sort by domestic slaughter count
    domestic_slaughter = domestic_slaughter.sort_values(by='Total Domestic(Nr)', ascending=False)
    states_order = domestic_slaughter['State'].tolist()
    
    # Reorder home slaughter data to match domestic slaughter
    home_slaughter['State'] = pd.Categorical(home_slaughter['State'], categories=states_order, ordered=True)
    home_slaughter = home_slaughter.sort_values(by='State')
    
    # Create interactive Plotly figure
    fig = go.Figure()
    
    # Add trace for domestic slaughter
    fig.add_trace(
        go.Bar(
            x=domestic_slaughter['State'],
            y=domestic_slaughter['Total Domestic(Nr)'],
            name='Domestic Slaughter',
            marker_color='green',
            text=domestic_slaughter['Total Domestic(Nr)'].apply(lambda x: f'{x:,}'),
            textposition='auto'
        )
    )
    
    # Add trace for home slaughter
    fig.add_trace(
        go.Bar(
            x=home_slaughter['State'],
            y=home_slaughter['Total Home(Nr)'],
            name='Home Slaughter',
            marker_color='lightgreen',
            text=home_slaughter['Total Home(Nr)'].apply(lambda x: f'{x:,}'),
            textposition='auto'
        )
    )
    
    # Update layout
    fig.update_layout(
        title=f'Distribution of Domestic and Home Slaughter by Region ({time_range[0]} to {time_range[1]})',
        xaxis_title='Region',
        yaxis_title='Number of Animals',
        yaxis_type='log',
        template='plotly_white',
        width=PLOT_FIGSIZE[0] * 50,  # Convert from inches to pixels
        height=PLOT_FIGSIZE[1] * 50,
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    
    # Update grid
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig
