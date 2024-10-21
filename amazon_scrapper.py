from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Set up Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Function to extract product data from a single page
def extract_product_data(soup):
    products = []
    
    for item in soup.select(".s-result-item"):
        name = item.select_one(".a-text-normal")
        price_whole = item.select_one(".a-price-whole")
        price_fraction = item.select_one(".a-price-fraction")
        rating = item.select_one(".a-icon-alt")
        reviews = item.select_one(".a-size-base")

        if name and price_whole:
            price = f"{price_whole.get_text(strip=True)}.{price_fraction.get_text(strip=True) if price_fraction else '00'}"
            product_data = {
                "Product Name": name.get_text(strip=True),
                "Price": price,
                "Rating": rating.get_text(strip=True) if rating else "No rating",
                "Reviews": reviews.get_text(strip=True) if reviews else "No reviews",
            }
            products.append(product_data)
    
    return products

# Function to scrape multiple pages of search results
def scrape_amazon(pages=3):
    all_products = []
    
    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        
        url = f"https://www.amazon.com/s?k=laptop&page={page}"
        driver.get(url)
        
        time.sleep(random.uniform(2, 5))  # Random delay to mimic human behavior
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = extract_product_data(soup)
        all_products.extend(products)
    
    driver.quit()  # Close the browser after scraping
    return all_products

# Scrape 3 pages of Amazon search results
product_data = scrape_amazon(pages=3)

# Convert the product data into a DataFrame
df = pd.DataFrame(product_data)

# Save the data to a CSV file
df.to_csv("amazon_products.csv", index=False)

print("Scraping completed and data saved to amazon_products.csv")
