import pandas as pd
import psycopg2


data = pd.read_csv('/Users/dilnazsaparbek/Desktop/project/parsing/products_data.csv')

data['Цена продукта'] = data['Цена продукта'].replace({r'[^\d.]': ''}, regex=True)

data['Цена продукта'] = pd.to_numeric(data['Цена продукта'], errors='coerce')

data['Цена продукта'].fillna(0, inplace=True)

print(data.head())


conn = psycopg2.connect(
    dbname="products_db", 
    user="postgres",     
    password="0000",      
    host="localhost",      
    port="5432"            
)

cursor = conn.cursor()


for _, row in data.iterrows():
    cursor.execute("""
        INSERT INTO products (name, category, price, city, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['Название продукта'], row['Категория продукта'], row['Цена продукта'], row['Город'], row['Статус']))


conn.commit()


cursor.close()
conn.close()

print("Data loaded to PostgreSQL successfully!")
