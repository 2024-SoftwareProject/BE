import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import requests
import pymysql
import django
from django.conf import settings
django.setup()
from bs4 import BeautifulSoup
from django.db import connection

from products_app.models import Product

def jungo_save_to_database(Pd_Market, Pd_Category, Pd_Name, Pd_Price, Pd_IMG, Pd_URL):
    product = Product(
        Pd_Market=Pd_Market,
        Pd_Category=Pd_Category,
        Pd_Name=Pd_Name,
        Pd_Price=Pd_Price,
        Pd_IMG=Pd_IMG,
        Pd_URL=Pd_URL
    )
    product.save()

# def jungo_get_products_by_category(query):
#     products = Product.objects.filter(Pd_Category=query)
#     return products

def jungo_search(query):
    with connection.cursor() as cursor:
        pages_to_crawl = 5
        Pd_Market='중고나라'
        item_name = query
        search_query = item_name.replace(" ", "")
        Pd_Category= search_query
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        for page in range(1, pages_to_crawl + 1):
            url = f"https://web.joongna.com/search/{search_query}?page={page}"
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")

            Name = soup.find_all("h2", class_="line-clamp-2 text-sm md:text-base text-heading")
            Price = soup.find_all("div", class_="font-semibold space-s-2 mt-0.5 text-heading lg:text-lg lg:mt-1.5")
            Image = soup.find_all("img", class_="bg-gray-300 object-cover h-full group-hover:scale-105 w-full transition duration-200 ease-in rounded-md")
            URL = soup.find_all("a", class_="group box-border overflow-hidden flex rounded-md cursor-pointer pe-0 pb-2 lg:pb-3 flex-col items-start transition duration-200 ease-in-out transform bg-white")


            for name, price, image, url in zip(Name, Price, Image, URL):
                Pd_Name = name.text.strip()

                if(Pd_Name.find("삽")!= -1):
                    continue
                if(Pd_Name.find("케이스")!= -1):
                    continue
                if(Pd_Name.find("매입")!= -1):
                    continue
                if(Pd_Name.find("구매")!= -1):
                    continue
                
                Pd_Price = price.text.strip()[:-1] #원을 빼고 
                Pd_Price = Pd_Price.replace(',', '') #,을 제거하고 
                try:
                    Price = int(Pd_Price) #정수로 변환 
                    print("가격: ",price)
                except ValueError:
                    print("가격 형식이 올바르지 않습니다.")

                
                Pd_IMG = image['src']
                Pd_URL = "https://web.joongna.com" + url['href']
                jungo_save_to_database(Pd_Market, Pd_Category, Pd_Name, Pd_Price, Pd_IMG, Pd_URL)
        connection.close()