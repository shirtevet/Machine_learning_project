# All Libraries
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd 
import requests
import time 
# User Agent File
My_User_Agent  = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
headers = {
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': My_User_Agent,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.amazon.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")

# Driver Setting to notice. 
try:driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
except:driver = webdriver.Chrome()

# Looping Through Pages
listofdict = list()
Listing_count= 7000 
Listing_start = 1
Script_Break = False
Full_Break = False
pages = range(1,100)
for page in pages:
    if Full_Break == True:
        break

    driver.get('https://www.amazon.com/')
    time.sleep(2)
    Page_URL = f"https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A16225009011%2Cn%3A541966&page={page}&qid=1709158259&ref=sr_pg_1"
    driver.get(Page_URL)
    time.sleep(3)

    response = driver.page_source
    soup = BeautifulSoup(response, "html.parser")

    Results = soup.find_all('div',class_='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20')
    # Looping Through Each Product
    for data in Results:
        if Script_Break == True:
            Full_Break = True
            break

        try:
            Product_Link = data.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal').get('href')
            Full_Link = 'https://www.amazon.com' + Product_Link

            driver.get(Full_Link)
            time.sleep(2)

            Product_response = driver.page_source
            Product_Soup = BeautifulSoup(Product_response, "html.parser")

            #Getting Data 
            product_name = Product_Soup.find('span', id="productTitle").text.strip()
            product_price = Product_Soup.find('span', class_='aok-offscreen').text
            try:
                product_Description = Product_Soup.find('div', id='aplus').text.strip()
            except:
                product_Description = Product_Soup.find('div', id='apm-brand-story-carousel').text.strip()
            review_link = Product_Soup.find('a', class_='a-link-emphasis a-text-bold').get('href')
      
            review_url = 'https://www.amazon.com' + review_link
            driver.get(review_url)
            time.sleep(2)

            review_response = driver.page_source
            review_soup = BeautifulSoup(review_response, "html.parser")
            all_reviews = review_soup.find_all('div', class_='a-section review aok-relative')
            
            for review_data in all_reviews:
                print('I am here')
                datadict = dict()
                datadict['Product Name'] = product_name
                datadict['Product Price'] = product_price
                datadict['Product Description'] = product_Description
                datadict['Product ID'] = Full_Link.split('/')[5]
                datadict['Brand'] =review_soup.find('a', class_='a-size-base a-link-normal').text
                datadict['Rating'] =review_data.find('span', class_='a-icon-alt').text.split(' ')[0]
                datadict['Date'] =review_data.find('span', class_='a-size-base a-color-secondary review-date').text.split(' on ')[1]
                datadict['customer reviews'] =review_data.find('span', class_='a-size-base review-text review-text-content').text.strip()
                print(datadict)
                listofdict.append(datadict)
                print('Listing Number......', Listing_start)
                if Listing_start >= Listing_count:
                    Script_Break = True
                    break
                Listing_start = Listing_start+1
        except:
            pass

df = pd.DataFrame.from_dict(listofdict)
path = 'Amazon_Data.csv'
df.to_csv(path ,index=False)
print(f'Data Saved in {path}')


        

