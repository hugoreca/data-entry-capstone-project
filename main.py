import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import re

# Constants and variables to use
FORMS_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeo5ypHZjYoU-0ekosKXx61IFV-E_iM0Eitqi_7MliUYg7WFw/viewform?usp=sf_link "
ZILLOW_WEBPAGE = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.59762801705124%2C%22east%22%3A-122.26902998294877%2C%22south%22%3A37.68198729218142%2C%22north%22%3A37.86847800956563%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
PREFIX = "https://www.zillow.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
    "Accept-Language": "en-US"
}
# Selenium related variables
BINARY_LOCATION = "C:\Program Files\BraveSoftware\Brave-Browser\Application\\brave.exe"
PATH = "C:\Development\chromedriver.exe"
options = Options()
options.binary_location = BINARY_LOCATION
driver = webdriver.Chrome(options=options, executable_path=PATH)

# Get the Html code using requests module
zillow_request = requests.get(url=ZILLOW_WEBPAGE, headers=headers)

# Parse the html code with BS4
soup = BeautifulSoup(zillow_request.content, "html.parser")

# Get the list of all of the properties, used list comprehension with an else statement nested and concatenated the relative references with the PREFIX
properties_links = [(item['href'] if item['href'][:22] == PREFIX else PREFIX + item['href']) for item in soup.find_all(name="a", attrs={"class": "list-card-link list-card-link-top-margin list-card-img"})]

# Get the list of all the prices, used regex split method to split the "/" or "+" characters
prices = [re.split('[/+]', item.getText())[0] for item in soup.find_all(name="div", attrs={"class": "list-card-price"})]

# Get the list of all of the addresses
addresses = [item.getText() for item in soup.find_all(name="address", attrs={"class": "list-card-addr"})]

driver.get(FORMS_URL)

for i in properties_links:
    idx = properties_links.index(i)
    # TODO 1: Complete and send all of the fields
    first_answer = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    first_answer.send_keys(addresses[idx])
    second_answer = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    second_answer.send_keys(prices[idx])
    third_answer = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    third_answer.send_keys(properties_links[idx])
    send_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div').click()
    # TODO 2: Send another answer
    send_another = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()
    time.sleep(1)

driver.quit()



