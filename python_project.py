#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install selenium')


# In[8]:


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from flask import Flask, render_template, request
import os
from selenium.webdriver.chrome.options import Options
import time
import re
import warnings
warnings.filterwarnings('ignore')


# In[9]:


class mobile_prices():
    
    
    # user input of mobile
#     def __init__(self):
#         self.name = input("Enter Mobile Name here: ")
        
        
    # scraping Flipkart
    def flipkart(self, product_name):
        url = "https://www.flipkart.com/"
        query = "search?q=" + product_name
        url = url + query
        
        site = 'Flipkart'
        
        result = requests.get(url)
        soup = BeautifulSoup(result.content, 'html.parser')
        
        self.flipkart_details = []
        if soup.find_all(class_='_31qSD5'):
            for i,mob in enumerate(soup.find_all(class_ = '_31qSD5')):
                try:
                    name = mob.find(class_ = '_3wU53n').text.strip()
                    price = mob.find(class_ = '_1vC4OE _2rQ-NK').text.strip()
                    try:
                        img_det = re.findall("keySpecs(.*?)jpeg", result.text)[i]
                        details = re.findall("\[\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\".*url\":\"(.*)", img_det)[0]
                        url = details[5]
                        url = re.sub("{@width}|{@height}", '250', url) + 'jpeg'
                    except:
                        url = ''
                    try:
                        prod_url = mob.attrs['href']
                        prod_url = "https://www.flipkart.com" + prod_url
                    except:
                        prod_url = ''
                    try:
                        rating = mob.find('div', class_ = 'hGSR34 _2beYZw').text.strip()
                    except:
                        rating = ''
                    try:
                        no_of_ratings = re.findall('(.*)Ratings',mob.find_all('span', class_ = '_38sUEc')[0].text)[0].strip()
                    except:
                        no_of_ratings = ''
    #                 no_of_reviews = re.findall('\xa0&\xa0(.*)Reviews',mob.find_all('span', class_ = '_38sUEc')[0].text)[0].strip()
                    self.flipkart_details.append([name, price, rating, no_of_ratings, site, url, prod_url])
#                     print(site, name, price, url, prod_url)
                except:
                    pass
        else:
            for i,mob in enumerate(soup.find_all('div', class_='_3liAhj _1R0K0g')):
                try:
                    name = mob.find(class_ = '_2cLu-l').text.strip()
                    price = mob.find(class_ = '_1vC4OE').text.strip()
                    try:
                        img_det = re.findall("keySpecs(.*?)jpeg", result.text)[i]
                        details = re.findall("\[\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\",\"(.*?)\".*url\":\"(.*)", img_det)[0]
                        url = details[5]
                        url = re.sub("{@width}|{@height}", '250', url) + 'jpeg'
                    except:
                        url = ''
                    try:
                        prod_url = mob.find(class_ = 'Zhf2z-')
                        prod_url = prod_url.attrs['href']
                        prod_url = "https://www.flipkart.com" + prod_url 
                    except:
                        prod_url = ''
                    try:
                        rating = mob.find(class_ = 'hGSR34 _2beYZw').text.strip()
                    except:
                        rating = ''
                    try:
                        no_of_ratings = mob.find(class_ = '_38sUEc').text.strip('()')
                    except:
                        no_of_ratings = ''
                    self.flipkart_details.append([name, price, rating, no_of_ratings, site, url, prod_url])
#                     print(site, name, price, url, prod_url)
                except:
                    pass
        return True
                
    # scraping Snapdeal    
    def snapdeal(self, product_name):
        url = "https://www.snapdeal.com/"
        query = "search?keyword=" + product_name
        url = url + query
        
        site = 'Snapdeal'
        
        result = requests.get(url)
        soup = BeautifulSoup(result.content, 'html.parser')
        
        self.snapdeal_details = []
        for mob in soup.find_all(class_='col-xs-6'):
            try:
                name = mob.find(class_ = 'product-title').text.strip()
                price = mob.find(class_ = 'lfloat product-price').text.strip()
                try:
                    prod_url = mob.find(class_ = 'dp-widget-link')
                    prod_url = prod_url.attrs['href']
                except:
                    prod_url = ''
                try:
                    rating = re.findall('width:(.*?)">',str(mob.find(class_ = 'filled-stars')))[0]
                except:
                    rating = ''
                try:
                    no_of_ratings = mob.find(class_ = 'product-rating-count').text.strip('()')
                except:
                    no_of_ratings = ''
                try:
                    url = mob.find(class_ = 'product-image')
                    url = url.attrs['srcset']
                except:
                    url = ''
                self.snapdeal_details.append([name, price, rating, no_of_ratings, site, url, prod_url])
#                 print(site, name, price, prod_url)
            except:
                pass
        return True
            
    # scraping PaytmMall    
    def paytmmall(self, product_name):
        url = "https://paytmmall.com/"
        query = "shop/search?q=" + product_name
        url = url + query
        
        result = requests.get(url)
        soup = BeautifulSoup(result.content, 'html.parser')
        
        site = 'PaytmMall'
        
        self.paytmmall_details = []
        for mob in soup.find_all('div', class_='_3WhJ'):
            try:
                name = mob.find(class_ = '_2apC').text.strip()
                price = mob.find(class_ = '_1kMS').text.strip()
                try:
                    prod_url = mob.find('a')
                    prod_url = prod_url.attrs['href']
                    prod_url = "https://paytmmall.com" + prod_url
                except:
                    prod_url = ''
                try:
                    cashback = mob.find(class_ = '_27VV').text.strip()
                except:
                    cashback = ''
                try:
                    url = mob.find('img')
                    url = url.attrs['src']
                except:
                    url = ''
                self.paytmmall_details.append([name, price, cashback, site, url, prod_url])
#                 print(site, name, price, prod_url)
            except:
                pass
        return True
    
    # scraping ShopClues
    def shopclues(self, product_name):
        url = "https://www.shopclues.com/"
        query = "search?q=" + product_name
        url = url + query
        
        site = 'Shopclues'
        
        result = requests.get(url)
        soup = BeautifulSoup(result.content, 'html.parser')
        
        self.shopclues_details = []
        for mob in soup.find_all('div', class_='column col3 search_blocks'):
            try:
                name = mob.find('h2').text.strip()
                price = mob.find(class_ = 'p_price').text.strip()
                try:
                    prod_url = mob.find('a')
                    prod_url = prod_url.attrs['href']
                    prod_url = "http:" + prod_url
                except:
                    prod_url = ''
                try:
                    url = mob.find('img')
                    url = url.attrs['data-img']
                except:
                    url = ''
                self.shopclues_details.append([name, price, site, url, prod_url])
#                 print(site, name, price, prod_url)
            except:
                pass
        return True
            
    # scraping TataCliq
    def tatacliq(self, product_name):
        url = "https://www.tatacliq.com/"
        query = "search/?text=" + product_name
        url = url + query
        
        site = 'TataCliq'
        
        options = Options()
        options.add_argument('--headless')
#         options.add_argument("--window-size=1000,600")

        # download chromedriver form internet for Chrome selenium and give the path here
        CHROMEDRIVER_PATH = 'D:\chromedriver'
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
        driver.get(url)
        
        self.tatacliq_details = []
        for mob in driver.find_elements_by_class_name('LK_htgvFpS2PUMylIQlif'):
            try:
                name = mob.find_elements_by_tag_name('h3')[1].text.strip()
                price = mob.find_elements_by_tag_name('h3')[2].text.strip()
                self.tatacliq_details.append([name, price, site])
#                 print(site, name, price)
            except:
                pass
        return True
    
    # scraping Amazon    
    def amazon(self, product_name):
#         url = "https://www.amazon.in/"
        
        site = 'Amazon'

        url = "https://www.amazon.in/"
        query = "s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=" + product_name
        url = url + query
        
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        r = requests.get(url, headers = header)
        
        driver = BeautifulSoup(r.content)
        self.amazon_details = []
        
        for mob in driver.find_all(class_ = 's-item-container'):
            try:
                name = mob.find('h2', class_ = 'a-size-base').text.strip()
                price = mob.find('span', class_ = 'a-size-base').text.strip()
                try:
                    prod_url = mob.find(class_ = 'a-link-normal')
                    prod_url = prod_url.attrs['href']
                    if re.search('url=https', prod_url):
                        prod_url = "https://www.amazon.in" + prod_url
                except:
                    prod_url = ''
                try:
                    url = mob.find('img')
                    url = url.attrs['src']
                except:
                    url = ''
                self.amazon_details.append([name, price, site, url, prod_url])
#                 print(site, name, price, prod_url)
            except:
                try:
                    name = mob.find('h2', class_ = 'a-size-medium').text.strip()
                    price = mob.find('span', class_ = 'a-size-base').text.strip()
                    try:
                        prod_url = mob.find(class_ = 'a-link-normal')
                        prod_url = prod_url.attrs['href']
                        if re.search('url=https', prod_url):
                            prod_url = "https://www.amazon.in" + prod_url
                    except:
                        prod_url = ''
                    try:
                        url = mob.find('img')
                        url = url.attrs['src']
                    except:
                        url = ''
                    self.amazon_details.append([name, price, site, url, prod_url])
#                     print(site, name, price, prod_url)
                except:
                    pass
        return True
    
    # combining and filtering all the scraped results
    def combine(self, product_name):
        
        # regex to remove products containing these keywords
        reg = 'cover|case|guard|glass|defender|stand|compatible|combo|accessory|headphone|headset|\stv\s|\sac\s|led|Refrigerator|washing|keyboard|door|monitor|inverter|machine|kettle|coin|bag|sandal|cable|plug|back'
        amazon = pd.DataFrame(self.amazon_details, columns= ['Name', 'Price', 'Site', 'Url', 'Product_Url'])
#         tatacliq = pd.DataFrame(self.tatacliq_details, columns= ['Name', 'Price', 'Site'])
        shopclues = pd.DataFrame(self.shopclues_details, columns= ['Name', 'Price', 'Site', 'Url', 'Product_Url'])
        paytmmall = pd.DataFrame(self.paytmmall_details, columns= ['Name', 'Price', 'Cashback', 'Site', 'Url', 'Product_Url'])
        snapdeal = pd.DataFrame(self.snapdeal_details, columns= ['Name', 'Price', 'Rating', 'No of Ratings', 'Site', 'Url', 'Product_Url'])
        flipkart = pd.DataFrame(self.flipkart_details, columns= ['Name', 'Price', 'Rating', 'No of Ratings', 'Site', 'Url', 'Product_Url'])
#         data = pd.concat([amazon , tatacliq , shopclues, paytmmall, snapdeal, flipkart])
        data = pd.concat([amazon, shopclues, paytmmall, snapdeal, flipkart])
        
        # converting price into string
        data.Price = data.Price.astype(str)
        
        # removing unnecessary symbols from price
        data.Price = data.Price.str.replace('₹|Rs.?|,|\..+','', case = False)
        data.Cashback = data.Cashback.str.replace('₹|Rs.?|,|.ashback|\..+','', case = False)
        
        # removing products containing certain keywords
        data = data[~data.Name.str.contains(reg, case = False)]
        
        # only keeping products containing our original query
        data = data[data.Name.str.contains(product_name, case = False)]
        
        # converting price into integer from string
        data.Price = data.Price.astype(int)
        
        # removing products having price less than the mean-2*std
        data = data[~(data.Price < data.Price.mean() - data.Price.mean()/2)]
#         data.to_csv(r'D:\Innominds\mobile_prices\\' + product_name + '.csv', index = False)
        data.sort_values(['Price'], inplace = True)
        data = data.head(1)
        ans = "{} on {} for Rs. {}".format(data.Name.iloc[0], data.Site.iloc[0], str(data.Price.iloc[0]))
        img = data.Url.iloc[0]
        url = data.Product_Url.iloc[0]
        answer = [img, ans, url]
#         ans = [data.Name.iloc[0], data.Site.iloc[0], str(data.Price.iloc[0])]
        
        return answer


# In[10]:


obj = mobile_prices()


# In[11]:


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hello", methods=["POST"])
def hello():
    print("coming here")
    if request.method = "POST":
        ques = request.form
        print(ques)

    # ques = "samsung-nokia-apple"
    ques = ques.split('-')
    ans = []
    for name in ques:
        name = name.strip()
        print(name)
        obj.flipkart(name)
        obj.snapdeal(name)
        obj.shopclues(name)
        obj.paytmmall(name)
        obj.amazon(name)
#         obj.tatacliq(name)
        ans.append(obj.combine(name))
    return render_template("hello.html", name = ans)

# @app.route("/more")
# def more():
#     print(an2)
#     return render_template("more.html",name=an2)

if __name__ == "__main__":
    app.run()

