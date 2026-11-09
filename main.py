import pandas as pd

df = pd.read_csv('data/data.csv', encoding='latin-1')

def data_exploration(df):
    print("Data Exploration:")
    print(df.head())
    print(df.shape)
    df.info()
    print(df.describe())
    print(df.columns)
    print(df.isna().sum().sum())
    print(df.duplicated().sum())

def basic_statistics(df):
    print("Basic Statistics:")
    print(f"Total Sales: {df['Sales'].sum():.2f}")
    print(f"Total Profit: {df['Profit'].sum():.2f}")
    print(f"Unique product categories: {df['Category'].nunique()}")

def category_summary(df):
    summary = df.groupby('Category').agg({
        'Sales': 'sum', 
        'Profit': 'sum'
    })

    summary['Margin %'] = (summary['Profit'] / summary['Sales']) * 100

    summary = summary.sort_values(by='Profit', ascending=False)

    return summary.round(2)

def furniture_subcategory_summary(df):
    furniture_summary = df[df['Category'] == 'Furniture'].groupby('Sub-Category').agg({
        'Sales': 'sum', 
        'Profit': 'sum'
    })

    furniture_summary['Margin %'] = (furniture_summary['Profit'] / furniture_summary['Sales']) * 100

    furniture_summary = furniture_summary.sort_values(by='Margin %', ascending=False)

    return furniture_summary.round(2)

