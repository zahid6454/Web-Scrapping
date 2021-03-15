from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Setting up PATH for Chrome Driver
PATH = 'C:\Program Files (x86)\chromedriver.exe'
# Setting up the Driver
driver = webdriver.Chrome(PATH)
# Hitting the GoDaddy Website URL
driver.get('https://sg.godaddy.com/')

try:
    # Waiting for the website to complete loading
    # Also, waiting to find the element with ID = 'domainToCheck'(Maximum Wait = 10 Sec)
    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'domainToCheck'))
    )
    # Typing "xyz" in the Search Box
    search.send_keys('xyz')
    # Executing the search
    search.send_keys(Keys.RETURN)

    try:
        # Waiting for the search result page to load
        # Also, waiting to find the element with ID = "spin-wrap"(Maximum Wait = 10 Sec)
        search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'spin-wrap'))
        )

        # Inside the search_results, finding element with class_name = "domain-name-text",
        # This element holds the domain name information.
        domain_names_raw = search_results.find_elements_by_class_name('domain-name-text')

        # Filtering the domain names
        domain_names = []
        domain_name = ''
        count = 0
        for i in range(len(domain_names_raw)):
            count += 1
            data = domain_names_raw[i].text
            domain_name = domain_name + data
            if count > 2:
                domain_names.append(domain_name)
                domain_name = ''
                count = 0

        # Inside the search_results, finding element with class_name = "dpp-price",
        # This element holds the domain price information.
        domain_prices_raw = search_results.find_elements_by_class_name('dpp-price')

        # Filtering the domain prices
        domain_prices = []
        domain_price = ''
        for i in range(len(domain_prices_raw)):
            domain_price = domain_prices_raw[i].text
            domain_price = domain_price.replace('$', '')
            domain_prices.append(domain_price)

        # Creating a Pandas Data Frame containing two columns ['Domain Name' and 'Domain Price ($)']
        # by combining the domain names list and domain prices list.
        df = pd.DataFrame(list(zip(domain_names, domain_prices)),
                          columns=['Domain Name', 'Domain Price ($)'])

        # Creating a CSV file out of the Pandas Data Frame and storing it in project Directory
        df.to_csv('Domain Name-Price Data Sheet.csv', index=False)

    except:
        driver.quit()
except:
    driver.quit()

driver.close()

