import pandas as pd

df = pd.read_csv('data/data.csv', encoding='latin-1')

def check_data_types(df):
    print("Data Types:")
    print(df.dtypes)

def convert_check_dates(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce', format='%m/%d/%Y')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce', format='%m/%d/%Y')

    print(df[['Order Date', 'Ship Date']].isna().sum().sum(), "rows have invalid dates.")

    delta = df['Ship Date'] - df['Order Date']
    print((delta < pd.Timedelta(0)).sum(), "rows have negative shipping time.")

    print("Maximum shipping time (days):", delta.dt.days.max())
    print("Minimum shipping time (days):", delta.dt.days.min())

convert_check_dates(df)