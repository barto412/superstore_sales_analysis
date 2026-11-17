import pandas as pd

#check data types of the columns
def check_data_types(df):
    print("Data Types:")
    print(df.dtypes)

def convert_dates(df):
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce', format='%m/%d/%Y')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce', format='%m/%d/%Y')

#check dates for invalid values and negative shipping time
def check_dates(df):
    print(df[['Order Date', 'Ship Date']].isna().sum().sum(), "rows have invalid dates.")

    delta = df['Ship Date'] - df['Order Date']
    print((delta < pd.Timedelta(0)).sum(), "rows have negative shipping time.")

    print("Maximum shipping time (days):", delta.dt.days.max())
    print("Minimum shipping time (days):", delta.dt.days.min())

def check_numeric_values(df):
    #check for negative or zero sales
    invalid_sales = (df['Sales'] <= 0).sum()
    print(invalid_sales, "rows have negative or zero sales.")

    #check for negative or zero quantity
    invalid_quantity = (df['Quantity'] <= 0).sum()
    print(invalid_quantity, "rows have negative or zero quantity.")

    #check for negative or over 100% discount
    invalid_discount = ((df['Discount'] < 0).sum() | (df['Discount'] > 1).sum())
    print(invalid_discount, "rows have negative or over 100% discount values.")

    #check for negative profit
    negative_profit = (df['Profit'] < 0).sum()
    negative_profit_percentage = (negative_profit / len(df)) * 100
    print(negative_profit, "rows have negative profit values.")
    print(f"Percentage of rows with negative profit: {negative_profit_percentage:.2f}%")
    
if __name__ == "__main__":
    df = pd.read_csv('data/data.csv', encoding='latin-1')
    
    convert_dates(df)
    check_data_types(df)
    check_dates(df)
    check_numeric_values(df)