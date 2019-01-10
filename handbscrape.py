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
driver = webdriver.Chrome(executable_path='/Users/aayush/Documents/Work/Scraper/chromedriver')
driver.get(base_url)
#HTML_Content
home_html = driver.page_source
soup  = BeautifulSoup(home_html,'lxml')
# Get all the categories and their root URLS
categories=[]
hier=[]
category_container = soup.find('div', class_='category-cartridge-desktop') 
# print(category_container)
for links in  category_container.find_all('a',href=True):
    # Categories URLs
    categories.append(base_url+ links['href'])
# print(categories)
single_url = categories[1]
driver.get(single_url)
#HTML_Content
single_html = driver.page_source
# close connection
page_soup = BeautifulSoup(single_html,'lxml')
# print(page_soup)
# Get the View All Link
if page_soup.find('a',alt='View All',href=True):
    all_link_soup = page_soup.find('a',alt='View All',href=True)
    # Convert text into actual link
    all_link = base_url+ all_link_soup['href']
elif page_soup.find('a',alt='Shop All',href=True):
    all_link_soup = page_soup.find('a',alt='Shop All',href=True)
else:
    pass
# Convert text into actual link
all_link = base_url+ all_link_soup['href']
driver.get(all_link)
# HTML Content of Products Listing Page
try:
    element = WebDriverWait(driver,10).until(
        EC.presence_of_all_elements_located((By.ID, "ajaxLoaded"))
    )
except:
    print("Nope")
    driver.quit()

product = driver.find_element_by_xpath('//*[@id="scroll-after-filter-apply"]/div[2]/section/div/ul').text
print(product)
# product_soup= BeautifulSoup(product,'lxml')
# print(product_soup)
