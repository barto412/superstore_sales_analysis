import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_cleaning import convert_dates

df = pd.read_csv('data/data.csv', encoding='latin-1')

def data_exploration(df):
    print("Data Exploration:")
    print(df.head())
    print(df.shape)
    df.info()
    print(df.columns)

def basic_statistics(df):
    print("Basic Statistics:")
    print(f"Total Sales: {df['Sales'].sum():.2f}")
    print(f"Total Profit: {df['Profit'].sum():.2f}")
    print(f"Unique product categories: {df['Category'].nunique()}")

#summary by category and sub-category (sales, profit, margin %)
def category_summary(df):
    category_summary = df.groupby('Category').agg({
        'Sales': 'sum', 
        'Profit': 'sum',
        'Discount': 'mean'
    })
    category_summary['Margin %'] = (category_summary['Profit'] / category_summary['Sales']) * 100
    category_summary['Negative profit count'] = df[df['Profit'] < 0].groupby('Category')['Profit'].count()
    category_summary['% of negative profit'] = (category_summary['Negative profit count'] / df.groupby('Category')['Profit'].count()) * 100
    category_summary = category_summary.sort_values(by='Margin %', ascending=False)
    print("\nCategory Summary:")
    print(category_summary.round(2))

    subcategory_summary = df.groupby(['Category', 'Sub-Category']).agg({
        'Sales': 'sum', 
        'Profit': 'sum',
        'Discount': 'mean'
    })
    subcategory_summary['Margin %'] = (subcategory_summary['Profit'] / subcategory_summary['Sales']) * 100
    subcategory_summary['Negative profit count'] = df[df['Profit'] < 0].groupby(['Category', 'Sub-Category'])['Profit'].count()
    subcategory_summary['% of negative profit'] = (subcategory_summary['Negative profit count'] / df.groupby(['Category', 'Sub-Category'])['Profit'].count()) * 100
    subcategory_summary['Negative profit count'] = subcategory_summary['Negative profit count'].fillna(0).astype(int)
    subcategory_summary['% of negative profit'] = subcategory_summary['% of negative profit'].fillna(0)
    subcategory_summary = subcategory_summary.sort_values(by=['Category', 'Margin %'], ascending=[True, False])
    print("\nSub-Category Summary:")
    print(subcategory_summary.round(2))

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

def product_summary(df):
    convert_dates(df)
    df['Year'] = df['Order Date'].dt.year

    #summary by product (sales, profit, margin %, negative profit count, % of negative profit)
    product_sales_summary = df.groupby('Product Name').agg({
        'Category': 'first',
        'Sub-Category': 'first',
        'Sales': 'sum', 
        'Profit': 'sum',
        'Discount': 'mean'
    })
    product_sales_summary['Margin %'] = (product_sales_summary['Profit'] / product_sales_summary['Sales']) * 100
    product_sales_summary['Negative profit count'] = df[df['Profit'] < 0].groupby('Product Name')['Profit'].count()
    product_sales_summary['Negative profit count'] = product_sales_summary['Negative profit count'].fillna(0).astype(int)
    product_sales_summary['% of negative profit'] = (product_sales_summary['Negative profit count'] / df.groupby('Product Name')['Profit'].count()) * 100
    product_sales_summary = product_sales_summary.sort_values(by='Negative profit count', ascending=False)
    print("\nProduct Sales Summary:")
    print(product_sales_summary.head(10).round(2))

    #specific product summary (change the product name to analyze a different product)
    specific_product = df[df['Product Name'] == 'Hon 61000 Series Interactive Training Tables']
    specific_product_summary = specific_product.groupby('Year').agg({
        'Sales': 'sum', 
        'Profit': 'sum',
    })
    specific_product_summary['Product Count'] = specific_product.groupby('Year')['Product Name'].count()
    specific_product_summary['Margin %'] = (specific_product_summary['Profit'] / specific_product_summary['Sales']) * 100
    specific_product_summary['Average profit per year'] = specific_product_summary['Profit'] / specific_product_summary['Product Count']
    print("\nSpecific Product Summary:")
    print(specific_product_summary.round(2))

product_summary(df)