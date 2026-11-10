import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    print("Furniture Sub-Category Summary:")
    print(furniture_summary.round(2))

    discount_mean_subcategory = df[(df['Category'] == 'Furniture')].groupby('Sub-Category').agg({
        'Discount': 'mean'
    })
    discount_mean_subcategory = discount_mean_subcategory.sort_values(by='Discount', ascending=True)
    print("Average Discount by Category:")
    print(discount_mean_subcategory.round(2))

    tables_discount_summary = df[(df['Category'] == 'Furniture') & (df['Sub-Category'] == 'Tables')].groupby('Discount').agg(
        Sales = ('Sales', 'sum'),
        Profit = ('Profit', 'sum'),
        Row_Count = ('Row ID', 'count')
    )
    tables_discount_summary['Margin %'] = (tables_discount_summary['Profit'] / tables_discount_summary['Sales']) * 100
    print("Furniture Discount Summary for Tables:")
    print(tables_discount_summary.round(2))

    #chart setup
    x = tables_discount_summary.index * 100
    y = tables_discount_summary['Margin %']

    colors = ['green' if margin >= 0 else 'red' for margin in y]

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(x, y, color=colors, width=5)
    ax.bar_label(bars, fmt='%.1f%%', padding=3)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_xlabel('Discount (%)')
    ax.set_ylabel('Margin %')
    ax.set_title('Margin % by Discount for Tables')
    ax.set_ylim(-100, 40)

    plt.tight_layout()
    plt.savefig('charts/tables_margin_by_discount.png', dpi=300, bbox_inches='tight')
    plt.show()

furniture_subcategory_summary(df)