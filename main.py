import pandas as pd
import matplotlib.pyplot as plt

# STEP 1: LOAD DATA
df = pd.read_csv("superstore.csv")

# Clean column names (VERY IMPORTANT)
df.columns = df.columns.str.strip()

print("Columns in dataset:")
print(df.columns)

# STEP 2: BASIC INFO

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nSummary Statistics:")
print(df.describe())


# STEP 3: DATA CLEANING
df.dropna(inplace=True)

# Fix date format
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

# Create Month column
df['Month'] = df['Order Date'].dt.month

print("\nCleaned Data:")
print(df.head())

# STEP 4: ANALYSIS

# Total Sales
print("\nTotal Sales:", df['Sales'].sum())

# Sales by Category
print("\nSales by Category:")
print(df.groupby('Category')['Sales'].sum())

# Monthly Sales
print("\nMonthly Sales:")
print(df.groupby('Month')['Sales'].sum())

# Sales by Region
print("\nSales by Region:")
print(df.groupby('Region')['Sales'].sum())

# Top 10 Products
print("\nTop 10 Products by Sales:")
print(df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10))


# STEP 5: PROFIT ANALYSIS (SAFE)


if 'Profit' in df.columns:
    print("\nProfit by Category:")
    print(df.groupby('Category')['Profit'].sum())
else:
    print("\n⚠️ Profit column not found in dataset")


# STEP 6: VISUALIZATION


# Sales by Category
df.groupby('Category')['Sales'].sum().plot(kind='bar')
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.xticks(rotation=0)
plt.show()

# Monthly Sales Trend
df.groupby('Month')['Sales'].sum().plot(kind='line', marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show()

# Sales by Region (Pie Chart)
df.groupby('Region')['Sales'].sum().plot(kind='pie', autopct='%1.1f%%')
plt.title("Sales by Region")
plt.ylabel("")
plt.show()

# Profit Graph (only if exists)
if 'Profit' in df.columns:
    df.groupby('Category')['Profit'].sum().plot(kind='bar')
    plt.title("Profit by Category")
    plt.show()