from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


driver = webdriver.Chrome()

url = "https://kingfisher.kz/"


driver.get(url)


WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "popupBtn_city")))


products_data = []

try:
    
    city_element = driver.find_element(By.CLASS_NAME, "popupBtn_city")
    city = city_element.text.strip()

   
    categories = driver.find_elements(By.CSS_SELECTOR, ".topMenu > li.dropmenu")
    print(f"Найдено категорий: {len(categories)}")

    
    categories_data = []
    for category in categories:
        category_name = category.find_element(By.TAG_NAME, "span").text.strip()
        subcategories = category.find_elements(By.CSS_SELECTOR, ".submenu > li > a")

        for subcategory in subcategories:
            subcategory_name = subcategory.text.strip()
            subcategory_link = subcategory.get_attribute("href")
            categories_data.append((category_name, subcategory_name, subcategory_link))

    print(f"Собрано {len(categories_data)} подкатегорий.")

    
    for category_name, subcategory_name, subcategory_link in categories_data:
        print(f"Переход к подкатегории: {subcategory_name} ({subcategory_link})")
        driver.get(subcategory_link)

        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "goodsBlock")))

       
        products = driver.find_elements(By.CLASS_NAME, "goodsBlock")
        print(f"Найдено продуктов в подкатегории {subcategory_name}: {len(products)}")

        for product in products:
            try:
                product_name = product.find_element(By.CLASS_NAME, "title").text.strip()
                product_price = product.find_element(By.CLASS_NAME, "new").text.strip()
                product_status = product.find_element(By.CLASS_NAME, "stickerPosition").text.strip() if product.find_elements(By.CLASS_NAME, "stickerPosition") else "Нет статуса"
                product_link = product.find_element(By.CLASS_NAME, "title").get_attribute("href")

                products_data.append({
                    "Название продукта": product_name,
                    "Категория продукта": category_name,
                    "Подкатегория продукта": subcategory_name,
                    "Цена продукта": product_price,
                    "Город": city,
                    "Ссылка на продукт": product_link,
                    "Статус": product_status
                })
            except Exception as e:
                print(f"Ошибка при обработке продукта: {e}")

except Exception as e:
    print(f"Ошибка при сборе данных: {e}")

finally:
    
    driver.quit()


df = pd.DataFrame(products_data)


output_csv_file = "products_data.csv"
df.to_csv(output_csv_file, index=False, encoding="utf-8")
print(f"Данные успешно сохранены в файл: {output_csv_file}")
