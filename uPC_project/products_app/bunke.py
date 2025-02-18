import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uPC_project.settings')

import django
from django.conf import settings
django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from products_app.models import Product
from category_app.models import Category


def bunke_save_to_database(Pd_Market, Pd_Category, Pd_Name, Pd_Price, Pd_IMG, Pd_URL):
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


def bunke_search(query):

# Selenium 구동
    browser = webdriver.Chrome()
    browser.implicitly_wait(time_to_wait=10)
    browser.get('https://m.bunjang.co.kr/')

    # 검색 입력
    itemname = query
    itemname = itemname.replace(' ', '')

    Pd_Market = "번개장터"
    Pd_Category = itemname

    # 페이지 순환을 위한 준비 및 Get요청 쿼리
    page = 0

    # 페이지 순환
    while True:
        page += 1
        if page == 3:
            break

        url = f"https://m.bunjang.co.kr/search/products?order=score&page={page}&q={itemname}"
        browser.get(url)
        print("*************", page, "번 Page**********************")
        
        # 대기
        WebDriverWait(browser, 10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "app")))
        
        # HTML 파싱
        html = browser.page_source
        html_parser = BeautifulSoup(html, features="html.parser")

        # 상품 이미지 태그 찾기
        list = html_parser.find_all(attrs={'alt':'상품 이미지'})

        for item in list:
            parent_div = item.parent.parent  # 이미지 태그의 부모 div 태그
            name = parent_div.find('div', class_='sc-kZmsYB bwuELN')  # 이름을 포함한 div 태그 선택 sc-hzNEM jbRqjn
            

            if(parent_div.find('div', class_='sc-gtfDJT brQSgh') or parent_div.find('div', class_='sc-RcBXQ gUYNYK') or parent_div.find('div', class_='sc-hzNEM jbRqjn')):
                continue

            if name:  # name이 None이 아니라면
                print("이름 : ", name.get_text())
                Pd_Name = name.get_text()

            if(item.parent.find(attrs={'alt':'판매 완료'}) or item.parent.find(attrs={'alt':'예약중'})):
                continue
            
            if(Pd_Name.find("삽")!= -1):
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
            if(Pd_Name.find("메모리북")!= -1):
                continue
            if(Pd_Name.find("폼")!= -1):
                continue
            if(Pd_Name.find("에어팟")!= -1):
                continue
            if(Pd_Name.find("쇼케이스")!= -1):
                continue
            if(Pd_Name.find("아이폰")!= -1):
                continue
            if(Pd_Name.find("갤럭시")!= -1):
                continue

            if(Pd_Name.find("섀도우")!= -1):
                continue
            if(Pd_Name.find("양도")!= -1):
                continue
            if(Pd_Name.find("메모리박스")!= -1):
                continue
            if(Pd_Name.find("USB")!= -1):
                continue
            if(Pd_Name.find("굿즈")!= -1):
                continue
            if(Pd_Name.find("시계")!= -1):
                continue
            if(Pd_Name.find("카메라")!= -1):
                continue
            if(Pd_Name.find("스위치")!= -1):
                continue
            if(Pd_Name.find("캠코더")!= -1):
                continue
            if(Pd_Name.find("보드게임")!= -1):
                continue
            if(Pd_Name.find("CD")!= -1):
                continue
            if(Pd_Name.find("프리즘스톤")!= -1):
                continue
            if(Pd_Name.find("포멘토")!= -1):
                continue
            if(Pd_Name.find("시계")!= -1):
                continue
            if(Pd_Name.find("ps4")!= -1):
                continue
            if(Pd_Name.find("디카")!= -1):
                continue
            if(Pd_Name.find("다이슨")!= -1):
                continue

            if(Pd_Name.find("계산기")!= -1):
                continue
            if(Pd_Name.find("패드")!= -1):
                continue
            if(Pd_Name.find("미니마우스")!= -1):
                continue
            if(Pd_Name.find("미키마우스")!= -1):
                continue

            if(Pd_Name.find("인형")!= -1):
                continue

            temp_price = parent_div.find('div', class_='sc-RcBXQ knGFtN')  # 이름을 포함한 div 태그 선택하고 즉시 텍스트 추출
            temp_price = temp_price.get_text()
            temp_price = temp_price.replace(',', '')  # 쉼표 삭제

            Pd_Price = temp_price
            print("가격 : ", Pd_Price )

            # 이미지 URL 출력
            if item.has_attr('src'):
                print("이미지 : {}".format(item['src']))
            else:
                print("이미지 속성을 찾을 수 없습니다.")

            Pd_IMG = item['src']
            
            # 링크 출력
            print("링크 : ", "https://m.bunjang.co.kr{}".format(parent_div.attrs['href']))

            Pd_URL = "https://m.bunjang.co.kr" + parent_div.attrs['href']
            print()

            bunke_save_to_database(Pd_Market, Pd_Category, Pd_Name, Pd_Price, Pd_IMG, Pd_URL)

    browser.quit()
