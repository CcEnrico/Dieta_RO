import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json

def scrape_products(urls, driver, output_file, links_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('[')
        
    for url in urls:
        start_time = time.time()

        driver.get(url)

        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-title__brand"))
            )
        except Exception as e:
            print(f"Errore nel caricamento dei prodotti da {url}: {e}")
            with open(links_file, 'r') as file:
                lines = file.readlines()
            with open(links_file, 'w') as file:
                for line in lines:
                    if line.strip() == url:
                        file.write(f"#{line}")
                    else:
                        file.write(line)
            continue

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        load_page_time = time.time()
        print(f"Time to load page and parse HTML from {url}: {load_page_time - start_time:.2f} seconds")

        brand_element = soup.find('h5', class_='product-title__brand')
        brand = brand_element.text.strip() if brand_element else 'Unknown'

        name_element = soup.find('h4', class_='product-title__name')
        name = name_element.text.strip() if name_element else 'Unknown'

        price_per_qty_element = soup.find('span', class_='product__price-per-qty')
        price_per_qty = price_per_qty_element.text.strip() if price_per_qty_element else 'Unknown'

        price_element = soup.find('span', class_='price__final')
        price = price_element.text.strip() if price_element else 'Unknown'

        nutritional_values = {}
        nutrition_table = soup.find('table', class_='product-information-table')

        if nutrition_table:
            headers = [header.text.strip() for header in nutrition_table.select('thead th')]
            rows = nutrition_table.select('tbody tr')
            for row in rows:
                columns = row.select('td')
                if len(columns) >= len(headers):
                    nutrient = columns[0].text.strip()
                    values = {headers[i]: columns[i].text.strip() for i in range(1, len(headers))}
                    nutritional_values[nutrient] = values

        print(f"Brand: {brand}")
        print(f"Name: {name}")
        print(f"Price per quantity: {price_per_qty}")
        print(f"Price: {price}")
        print(f"Nutritional values : {nutritional_values}")
        print(f"Url: {url}")

        product_data = {
            "Brand": brand,
            "Name": name,
            "Price per quantity": price_per_qty,
            "Price": price,
            "Nutritional values": nutritional_values,
            "Url": url
        }

        with open(output_file, 'a', encoding='utf-8') as file:
            json.dump(product_data, file, ensure_ascii=False, indent=4)
            file.write(',')
            file.write('\n')

        end_time = time.time()
        print(f"Tempo di caricamento per {url}: {end_time - start_time} secondi")

        with open(links_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(links_file, 'w', encoding='utf-8') as file:
            for line in lines:
                if line.strip() == url:
                    file.write(f"#{line}")
                else:
                    file.write(line)

def correct_json_formatting(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
        
        if content.endswith(','):
            content = content[:-1]
        
        if not content.startswith('['):
            content = '[' + content
        if not content.endswith(']'):
            content = content + ']'
        
        products = json.loads(content)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(products, file, ensure_ascii=False, indent=4)
        
        print(f"Formattazione del file JSON '{file_path}' corretta con successo.")
    except json.JSONDecodeError as e:
        print(f"Errore nella decodifica del JSON: {e}")
    except Exception as e:
        print(f"Errore durante la correzione del file JSON: {e}")

if __name__ == "__main__":
    output_file = 'prod.json'
    links_file = 'ref.txt'

    with open(links_file, 'r') as file:
        urls = [line.strip() for line in file.readlines() if not line.startswith('#')]
    
    options = Options()
    options.headless = True

    driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
    )

    correct_json_formatting(output_file)
    scrape_products(urls, driver, output_file, links_file)
    correct_json_formatting(output_file)

    # Rimuovi tutti gli # da ref.txt
    with open(links_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(links_file, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line.lstrip('#'))

    driver.quit()


