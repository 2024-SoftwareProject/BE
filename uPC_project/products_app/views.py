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

import statistics

#craling code 다운
from . import bunke
from . import jungo
from . import dangeun
from . import get_data

# 위시리스트 
from accounts_app.models import Wishlist

# search_history
from accounts_app.models import SearchHistory

#본격 서치 
def search_view(request):
    # URL에서 query 가져오기
    query = request.GET.get('query', '')
    edited_query = query.replace('sort', '')
    edited_query = edited_query.replace('+', '')
    edited_query = edited_query.replace(' ', '')
    edited_query = edited_query.replace('%20', '')

    # 검색 실행
    bunke.bunke_search(edited_query)
    jungo.jungo_search(edited_query)
    dangeun.dangeun_search(edited_query)

    outputDB = get_data.get_products_by_latest(edited_query)

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

    update_wishlist_status(request, page_obj)

    # search_history 데이터 저장
    save_search_history(request, edited_query)

    #제품의 값 중에서 최저가, 최대가, 평균 값 도출 목적 
    max_price_stat, min_price_stat, average_price_stat = calculate_price_stats(outputDB)
    # 결과를 렌더링하여 반환
    return render(request, 'products/search_result.html', {'query': query, 'outputDB':outputDB, 'page_obj': page_obj, 'paginator':paginator, 'page_start_number':page_start_number,'page_end_number':page_end_number, 'max_price_stat':max_price_stat, 'min_price_stat':min_price_stat, 'average_price_stat': average_price_stat})


def search_report_view(request):
    query = request.GET.get('query', '')
    edited_query = query.replace(' ', '')
    edited_query = edited_query.replace('+', '')
    edited_query = edited_query.replace('%20', '')

    sort = request.GET.get('sort', 'latest')
    min_price = request.GET.get('min', '0')
    max_price = request.GET.get('max', '3000000')
    market = request.GET.get('market', '')

    if not min_price:
        min_price = '0'
    if not max_price:
        max_price = '3000000'
    if not sort:
        sort = 'lastest'
    if not market:
        market= ''

    min_price = int(min_price)
    max_price = int(max_price)

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

    if market != '':
        outputDB = get_data.filter_products_by_market(outputDB, market)
    else:
        outputDB = outputDB

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

    # 위시리스트 목록 반영
    update_wishlist_status(request, page_obj)

    # search_history 데이터 저장
    save_search_history(request, edited_query)

    #결과에서 가격 정보 추출 
    max_price_stat, min_price_stat, average_price_stat = calculate_price_stats(outputDB)
    return render(request, 'products/search_result.html', {'query': query, 'outputDB':outputDB, 'page_obj': page_obj, 'paginator':paginator, 'page_start_number':page_start_number,'page_end_number':page_end_number, 'max_price_stat':max_price_stat, 'min_price_stat':min_price_stat, 'average_price_stat': average_price_stat})


def update_wishlist_status(request, page_obj):
    if request.user.is_authenticated:
        try:
            # 사용자의 위시리스트 가져옴
            wishlist = Wishlist.objects.get(user=request.user)
            # 위시리스트에 있는 상품의 ID 목록을 가져옴
            wishlist_product_ids = wishlist.products.values_list('Pd_IndexNumber', flat=True)

            for product in page_obj:
                product.is_in_wishlist = product.Pd_IndexNumber in wishlist_product_ids
        except Wishlist.DoesNotExist:
            # 위시리스트가 없는 경우, 모든 상품을 위시리스트에 없는 것으로 설정
            for product in page_obj:
                product.is_in_wishlist = False
    else:
        # 로그인하지 않은 사용자의 경우, 모든 상품을 위시리스트에 없는 것으로 설정
        for product in page_obj:
            product.is_in_wishlist = False


def save_search_history(request, keyword):
    if request.user.is_authenticated:
        # 로그인한 사용자의 경우, 검색 키워드를 SearchHistory 모델에 저장
        user = request.user
        search_history = SearchHistory(user=user, keyword=keyword)
        search_history.save()
        return "로그인한 사용자의 검색 기록이 저장되었습니다."
    else:
        # 로그인하지 않은 사용자
        return "로그인하지 않은 사용자입니다. 검색 기록이 저장되지 않습니다."

def calculate_price_stats(products):
    prices = [product.Pd_Price for product in products]
    if prices:
        max_price_stat = max(prices)
        min_price_stat = min(prices)
        average_price_stat = round(statistics.mean(prices))
    else:
        max_price_stat = None
        min_price_stat = None
        average_price_stat = None
    
    return max_price_stat, min_price_stat, average_price_stat