#기본 장고 veiw 관련 
from django.http import HttpResponse
from django.shortcuts import render

#crawling 관련 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

#페이지 나누기
from django.core.paginator import Paginator

#모델 
from products_app.models import Product

#craling code 다운
from . import bunke
from . import jungo
from . import dangeun
from . import get_data

#테스트용
def test(request):
    return HttpResponse("testtest")

#본격 서치 
def search_view(request):
    # URL에서 query 가져오기
    query = request.GET.get('query', '')

    # 검색 실행
    bunke.bunke_search(query)
    jungo.jungo_search(query)
    dangeun.dangeun_search(query)
    
    # # 검색 결과를 가져오기
    # outputDB = bunke.bunke_get_products_by_category(query)
    # outputDB = jungo.jungo_get_products_by_category(query)
    # outputDB = dangeun.dangeun_get_products_by_category(query)

    print("여기옴")

    edited_query = query.replace(' ', '')

    outputDB = get_data.get_products_by_price_asc(edited_query)

    # # 페이지 분할 과정
    paginator=Paginator(outputDB,48) 
    page_number=request.GET.get('page') 
    page_obj=paginator.get_page(page_number) 

    # 결과를 렌더링하여 반환
    return render(request, 'products/search_result.html', {'page_obj': page_obj})