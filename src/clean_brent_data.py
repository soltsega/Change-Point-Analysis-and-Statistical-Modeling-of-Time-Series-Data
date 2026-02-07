import pandas as pd
import numpy as np

def clean_brent_data():
    """
    Clean the Brent crude data by fixing header issues
    """
    # Read the data with header issue
    df = pd.read_csv('../data/raw/brent_crude_prices.csv')
    
    # Remove the problematic second row
    df = df.drop(0)
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Convert price columns to numeric
    price_columns = ['Close', 'High', 'Low', 'Open', 'Volume']
    for col in price_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Sort by date
    df = df.sort_values('Date')
    
    # Remove any rows with missing values
    df = df.dropna()
    
    # Save cleaned data
    df.to_csv('../data/raw/brent_crude_prices_clean.csv', index=False)
    
    print(f"Cleaned data shape: {df.shape}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Price range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
    print("\nFirst few rows:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    clean_brent_data()
