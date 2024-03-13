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
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
    edited_query = query.replace('sort', '')

    # 검색 실행
    bunke.bunke_search(query)
    jungo.jungo_search(query)
    dangeun.dangeun_search(query)
    
    # # 검색 결과를 가져오기
    # outputDB = bunke.bunke_get_products_by_category(query)
    # outputDB = jungo.jungo_get_products_by_category(query)
    # outputDB = dangeun.dangeun_get_products_by_category(query)

    print("여기옴")
    # get_data.HandlingDuplicates.remove_duplicates()

    outputDB = get_data.get_products_by_latest(query)

    # 페이지 분할 과정
    paginator=Paginator(outputDB,48)
    page=request.GET.get('page') 
    try:
        page_obj=paginator.page(page)
    except PageNotAnInteger:
        page=1
        page_obj=paginator.page(page) 
    except EmptyPage:
        page=paginator.num_pages
        page_obj=paginator.page(page)

    #현재 페이지가 몇번째 블럭인지
    current_block=int(((int(page)-1)/10)+1)
    #페이지 시작 번호
    page_start_number=((current_block-1)*10)+1
    #페이지 끝 번호
    page_end_number=page_start_number+10-1

    # 결과를 렌더링하여 반환
    return render(request, 'products/search_result.html', {'query': query, 'outputDB':outputDB, 'page_obj': page_obj, 'paginator':paginator, 'page_start_number':page_start_number,'page_end_number':page_end_number,})

def search_report_view(request):

    query = request.GET.get('query', '')
    edited_query = query.replace(' ', '')
    sort = request.GET.get('sort', 'latest')
    min_price = request.GET.get('min', '0')
    max_price = request.GET.get('max', '3000000')
    page = request.GET.get('page', '')

    if not min_price:
        min_price = '0'
    if not max_price:
        max_price = '3000000'

    if not sort:
        sort = 'lastest'

    min_price = int(min_price)
    max_price = int(max_price)


    print("RMfRMF")

    if  sort == 'latest':
        outputDB = get_data.get_products_by_latest(edited_query, min_price, max_price)
    elif sort == 'popularity':
        outputDB = get_data.get_products_by_popularity(edited_query, min_price, max_price)
    elif sort == 'price_low':
        outputDB = get_data.get_products_by_price_low(edited_query, min_price, max_price)
    elif sort == 'price_high':
        outputDB = get_data.get_products_by_price_high(edited_query, min_price, max_price)
    else:
        outputDB = get_data.get_products_by_latest(edited_query, min_price, max_price)
        print("eooror")

    paginator=Paginator(outputDB,48)
    page=request.GET.get('page') 
    try:
        page_obj=paginator.page(page)
    except PageNotAnInteger:
        page=1
        page_obj=paginator.page(page) 
    except EmptyPage:
        page=paginator.num_pages
        page_obj=paginator.page(page)

    #현재 페이지가 몇번째 블럭인지
    current_block=int(((int(page)-1)/10)+1)
    #페이지 시작 번호
    page_start_number=((current_block-1)*10)+1
    #페이지 끝 번호
    page_end_number=page_start_number+10-1

    return render(request, 'products/search_result.html', {'query': query, 'outputDB':outputDB, 'page_obj': page_obj, 'paginator':paginator, 'page_start_number':page_start_number,'page_end_number':page_end_number,})
