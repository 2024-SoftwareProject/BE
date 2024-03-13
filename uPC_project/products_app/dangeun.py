import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

#주로 나오는 당근 예외 경우
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from django.db.utils import OperationalError

import requests

from bs4 import BeautifulSoup
import pymysql
django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from products_app.models import Product

def dangeun_save_to_database(Pd_Market, Pd_Category, Pd_Name, Pd_Price, Pd_IMG, Pd_URL):
    # 이미 존재하는지 여부를 확인하여 중복 삽입 방지
    if not Product.objects.filter(Pd_Name=Pd_Name).exists():
        product = Product(
            Pd_Market=Pd_Market,
            Pd_Category=Pd_Category,
            Pd_Name=Pd_Name,
            Pd_Price=Pd_Price,
            Pd_IMG=Pd_IMG,
            Pd_URL=Pd_URL
        )
        product.save()

# def dangeun_get_products_by_category(query):
#     products = Product.objects.filter(Pd_Category=query)
#     return products


def dangeun_search(query):

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        itemname = query
        itemname = itemname.replace(' ', '')

        url = f"https://www.daangn.com/search/{itemname}/"
        browser = webdriver.Chrome()
        browser.get(url)

        Pd_Market = "당근마켓"
        Pd_Category = itemname

        current_products = set()
        product_list = []



        for i in range(10):

                element = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'more-btn'))
                )
                element.click() 
                print("버튼이 클릭")

                html = browser.page_source
                html_parser = BeautifulSoup(html, features="html.parser")
                product_list = html_parser.find_all('article', class_='flea-market-article flat-card')

            

        for item in product_list:

            #가격 데이터 추출
            a =item.find('p', class_='article-price')
            temp_price = a.get_text()

            # 가격 데이터 깔끔하게
            temp_price = temp_price.replace(' ', '')
            temp_price = temp_price.replace('원', '')
            temp_price = temp_price.replace('만', '0000')
            temp_price = temp_price.replace(',', '')

            #백오십, 백만원 이런 all한글 상품 제외
            try :
                Pd_Price = int(temp_price)

            except:
                continue

            # 나눔 상품 제외
            if(temp_price[0]=='나'):
                continue

            #판매 이름 추출
            a =item.find('span', class_='article-title')
            temp_name = a.get_text()

            Pd_Name = temp_name

            #전체
            if(Pd_Name.find("삽")!= -1):
                continue
            if(Pd_Name.find("케이스")!= -1):
                continue
            if(Pd_Name.find("매입")!= -1):
                continue
            if(Pd_Name.find("구매")!= -1):
                continue

            #메모리
            if(Pd_Name.find("시트")!= -1):
                continue
            if(Pd_Name.find("이벤트")!= -1):
                continue
            if(Pd_Name.find("포카")!= -1):
                continue
            if(Pd_Name.find("어몽어스")!= -1):
                continue
            if(Pd_Name.find("스티커")!= -1):
                continue
            if(Pd_Name.find("키링")!= -1):
                continue
            if(Pd_Name.find("닌텐도")!= -1):
                continue
            if(Pd_Name.find("북")!= -1):
                    continue
            if(Pd_Name.find("폼")!= -1):
                    continue

            #이미지 url 주소 추출
            a =item.find('img')
            temp_img = a['src']

            Pd_IMG = temp_img

            #상품 페이지 url 주소 추출
            a =item.find('a', class_='flea-market-article-link')
            temp_url = 'https://www.daangn.com' + a['href']

            Pd_URL = temp_url


            dangeun_save_to_database(Pd_Market, Pd_Category, Pd_Name, Pd_Price, Pd_IMG, Pd_URL)

    except (StaleElementReferenceException, TimeoutException, OperationalError) as e:
        print("예외 발생")
        print(e)



