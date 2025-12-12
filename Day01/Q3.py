
import pandas as pd

def simple_analyze_products(filename='Products.csv'):
    """Reads a CSV and performs a list of product analyses."""
    
    try:
        # a) Read the CSV (Try-except for error handling)
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return

    print("--- Product Analysis Results ---")

    # b) Print each row in a clean format
    print("\n1. All Products (Clean Format):\n" + df.to_string(index=False))

    # c) Total number of rows
    print(f"\n2. Total Number of Rows: {len(df)}")

    # d) Total number of products priced above $500 (Concise filtering)
    count_above_500 = (df['Price'] > 500).sum()
    print(f"3. Total Products Priced Above $500: {count_above_500}")

    # e) Average price of all products
    avg_price = df['Price'].mean()
    print(f"4. Average Price of All Products: ${avg_price:.2f}")

    # f) List all products belonging to a specific category (User input mocked)
    category_name = 'Apparel' # Replace with input() if needed
    category_products = df[df['Category'] == category_name]
    
    print(f"\n5. Products in Category '{category_name}':")
    if not category_products.empty:
        print(category_products.to_string(index=False))
    else:
        print("No products found in this category.")
    
    # g) Total quantity of all items in stock
    total_stock = df['StockQuantity'].sum()
    print(f"\n6. Total Quantity of All Items In Stock: {total_stock}")

# Run the function
simple_analyze_products()