from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# def product_scrape():
class AppURLOpener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
opener = AppURLOpener()
base_url = 'https://www.hollandandbarrett.com'
driver = webdriver.Chrome(executable_path=r'C:\Users\aayush.sharma\Documents\Scraping\chromedriver')
uClient = opener.open(base_url)
#HTML_Content
home_html = uClient.read()
# close connection
soup  = BeautifulSoup(home_html,'lxml',from_encoding='utf-8')
# Get all the categories and their root URLS
categories=[]
hier=[]
category_container = soup.find('div', class_='category-cartridge-desktop') 
# print(category_container)
for links in  category_container.find_all('a',href=True):
    # Categories URLs
    categories.append(base_url+ links['href'])
# print(categories)
for single_url in categories:
    uClient = opener.open(single_url)
    #HTML_Content
    single_html = uClient.read()
    # close connection
    page_soup = BeautifulSoup(single_html,'lxml',from_encoding='utf-8')
    # print(page_soup)
    # Get the View All Link
    all_link_soup = page_soup.find('a',alt='View All',href=True)
    # Convert text into actual link
    all_link = base_url+ all_link_soup['href']
    driver.get(all_link)
    uClient = opener.open(all_link)
    # HTML Content of Products Listing Page
    all_products_html = driver.page_source
    all_products_soup = BeautifulSoup(all_products_html,'lxml',from_encoding='utf-8')
    crumb =all_products_soup.find('div',class_='crumb')
    # print(crumb.text.split('\n'))
    a = crumb.findAll('a',itemprop='item')
    for items in a:
        # print(items.text.strip())
        hier.append(items.text.strip())
    hierarchy = " > ".join(hier)
    # Get the product hierarchy
    print(hierarchy)
    for products in  all_products_soup.find_all('div',class_='product-container'):
        name = products.find('h3', class_='prod-title')
        print(name.text.strip())
        price = products.find('div',class_='prod-price')
        print(price.text.strip())