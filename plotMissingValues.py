import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# AUXILIAR CODE TO DETECT MISSING DATES
def plot_sales_with_missing_dates(df, title, ax=None):
    """
    Plots sales over time and highlights missing dates.
    
    Parameters:
    - df: DataFrame with 'date' and 'Sales_$' columns
    - title: Plot title
    - ax: Matplotlib axis object (optional)
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create complete date range
    min_date = df['date'].min()
    max_date = df['date'].max()
    all_dates = pd.date_range(start=min_date, end=max_date, freq='D')
    
    # Find missing dates
    existing_dates = set(df['date'])
    missing_dates = [date for date in all_dates if date not in existing_dates]
    
    # Plot sales
    sns.lineplot(data=df, x='date', y='Sales_$', ax=ax, marker='o', label='Sales')
    
    # Highlight missing dates
    if missing_dates:
        for md in missing_dates:
            ax.axvline(x=md, color='red', alpha=0.3, linestyle='--')
    
    # Formatting
    ax.set_title(f"{title}\nMissing Dates: {len(missing_dates)}", fontsize=12)
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales ($)')
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Add legend
    if missing_dates:
        ax.legend(['Sales', 'Missing Dates'])
    else:
        ax.legend(['Sales'])
    
    return ax


plot_sales_with_missing_dates(df, "P28 z23")
plt.show()