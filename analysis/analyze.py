import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

def fetch_data_from_postgres():
    conn = psycopg2.connect(
        dbname="products_db",
        user="postgres",
        password="0000",  
        host="localhost",
        port="5432"
    )
    
   
    category_query = """
    SELECT category, COUNT(*) as count
    FROM products
    GROUP BY category
    ORDER BY count DESC
    """
    
    status_query = """
    SELECT status, COUNT(*) as count
    FROM products
    GROUP BY status
    ORDER BY count DESC
    """
    
    price_query = """
    SELECT category, 
           AVG(CAST(price AS FLOAT)) as average_price, 
           MIN(CAST(price AS FLOAT)) as min_price, 
           MAX(CAST(price AS FLOAT)) as max_price
    FROM products
    GROUP BY category
    ORDER BY average_price DESC
    """
   
    city_query = """
    SELECT city, COUNT(*) as count
    FROM products
    GROUP BY city
    ORDER BY count DESC
    """

    
    category_data = pd.read_sql_query(category_query, conn)
    status_data = pd.read_sql_query(status_query, conn)
    price_data = pd.read_sql_query(price_query, conn)
    city_data = pd.read_sql_query(city_query, conn)
    
    conn.close()
    
    return category_data, status_data, price_data, city_data

def visualize_data(category_data, status_data, price_data, city_data):
    # Визуализация распределения по категориям
    category_data.plot(kind='bar', x='category', y='count', legend=False)
    plt.title("Product Categories Distribution")
    plt.xlabel("Category")
    plt.ylabel("Number of Products")
    plt.tight_layout()
    plt.savefig('category_distribution.png')
    plt.show()

    # Визуализация распределения по статусам
    status_data.plot(kind='bar', x='status', y='count', legend=False)
    plt.title("Product Status Distribution")
    plt.xlabel("Status")
    plt.ylabel("Number of Products")
    plt.tight_layout()
    plt.savefig('status_distribution.png')
    plt.show()

    # Визуализация средней цены по категориям
    price_data.plot(kind='bar', x='category', y='average_price', legend=False)
    plt.title("Average Price by Category")
    plt.xlabel("Category")
    plt.ylabel("Average Price")
    plt.tight_layout()
    plt.savefig('average_price_by_category.png')
    plt.show()

    # Визуализация распределения по городам
    city_data.plot(kind='bar', x='city', y='count', legend=False)
    plt.title("Product Distribution by City")
    plt.xlabel("City")
    plt.ylabel("Number of Products")
    plt.tight_layout()
    plt.savefig('city_distribution.png')
    plt.show()

def print_summary(category_data, status_data, price_data, city_data):
    print("\n--- Category Distribution ---")
    print(category_data)
    
    print("\n--- Status Distribution ---")
    print(status_data)
    
    print("\n--- Price Statistics by Category ---")
    print(price_data)
    
    print("\n--- City Distribution ---")
    print(city_data)

if __name__ == "__main__":
    category_data, status_data, price_data, city_data = fetch_data_from_postgres()
    visualize_data(category_data, status_data, price_data, city_data)
    print_summary(category_data, status_data, price_data, city_data)
    print("Analysis complete. Charts saved and summary printed.")
