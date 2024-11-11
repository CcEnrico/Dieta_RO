import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

# Leggi gli URL da ref.txt, escludendo quelli che iniziano con #
with open('ref.txt', 'r') as file:
    urls = [line.strip() for line in file.readlines() if not line.startswith('#')]

# Imposta le opzioni di Firefox per la modalità headless
options = Options()
options.headless = True

# Inizializza WebDriver per connettersi al contenitore Selenium
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
)

for url in urls:
    # Inizia il timing
    start_time = time.time()

    # Apri l'URL
    driver.get(url)

    # Attendi fino a quando gli elementi del prodotto sono presenti
    try:
        # Attendi la presenza del contenitore principale che contiene i prodotti
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-title__brand"))
        )
    except Exception as e:
        print(f"Errore nel caricamento dei prodotti da {url}: {e}")
        with open('ref.txt', 'r') as file:
            lines = file.readlines()
        with open('ref.txt', 'w') as file:
            for line in lines:
                if line.strip() == url:
                    file.write(f"#{line}")
                else:
                    file.write(line)
        continue

    # Get the HTML content after elements are loaded
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Log time after loading page
    load_page_time = time.time()
    print(f"Time to load page and parse HTML from {url}: {load_page_time - start_time:.2f} seconds")

    brand_element = soup.find('h5', class_='product-title__brand')
    brand = brand_element.text.strip() if brand_element else 'Unknown'


    name_element = soup.find('h4', class_='product-title__name')
    name = name_element.text.strip() if name_element else 'Unknown'

    # price_per_qty_element = soup.select_one('span.product__price-per-qty')
    price_per_qty_element = soup.find('span', class_='product__price-per-qty')
    price_per_qty = price_per_qty_element.text.strip() if price_per_qty_element else 'Unknown'

    # price_element = soup.select_one('span.price__final')
    price_element = soup.find('span', class_='price__final')
    price = price_element.text.strip() if price_element else 'Unknown'

    # Extract nutritional values
    nutritional_values = {}
    # nutrition_table = soup.select_one('div.product__attribute-table table.product-information-table')
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

    # Open the file in append mode
    with open('prod.txt', 'a') as file:

        file.write(f"Brand: {brand}\n")
        file.write(f"Name: {name}\n")
        file.write(f"Price per quantity: {price_per_qty}\n")
        file.write(f"Price: {price}\n")
        file.write(f"Nutritional values: {nutritional_values}\n")
        file.write(f"Url: {url}\n")
        file.write('\n')

    # Log del tempo dopo il caricamento della pagina
    end_time = time.time()
    print(f"Tempo di caricamento per {url}: {end_time - start_time} secondi")

    # Se il caricamento è riuscito, aggiungi # all'inizio dell'URL in ref.txt
    with open('ref.txt', 'r') as file:
        lines = file.readlines()
    with open('ref.txt', 'w') as file:
        for line in lines:
            if line.strip() == url:
                file.write(f"#{line}")
            else:
                file.write(line)

# Chiudi il driver
driver.quit()
