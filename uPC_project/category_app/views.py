#기본 장고 veiw 관련 
from django.http import HttpResponse
from django.shortcuts import render

#페이지 나누기
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#모델 
from .models import CategoryProduct

#craling code 다운
from category_app import get_data

# 위시리스트 
from accounts_app.models import Wishlist

# search_history
from accounts_app.models import SearchHistory

import statistics

#본격 서치 
def search_view(request):
    # URL에서 query 가져오기
    categoryNumber = request.GET.get('category', '')
    categoryNumber = int(categoryNumber)
    print(categoryNumber)
    categoryName = get_data.get_minorname(categoryNumber)

    print("category1")
    print("cha")

    # 검색 실행
    if categoryNumber == 1:
        get_data.plus_products_from_product_model(1, "아이맥")
        get_data.plus_products_from_product_model(1, "데스크탑")
    elif categoryNumber == 2:
        get_data.plus_products_from_product_model(2, "맥북")
        get_data.plus_products_from_product_model(2, "노트북")
        print("22")
        get_data.plus_products_from_product_model(2, "삼성노트북")
        get_data.plus_products_from_product_model(2, "LG노트북")
    elif categoryNumber == 3:
        print("cha")
        get_data.plus_products_from_product_model(3, "CPU")
    elif categoryNumber == 4:
        get_data.plus_products_from_product_model(4, "메인보드")
    elif categoryNumber == 5:
        get_data.plus_products_from_product_model(5, "메모리")
    elif categoryNumber == 6:
        get_data.plus_products_from_product_model(6, "그래픽카드")
    elif categoryNumber == 7:
        get_data.plus_products_from_product_model(7, "SSD")
    elif categoryNumber == 8:
        get_data.plus_products_from_product_model(8, "HDD")
    elif categoryNumber == 9:
        get_data.plus_products_from_product_model(9, "케이스")
    elif categoryNumber == 10:
        get_data.plus_products_from_product_model(10, "파워")
    elif categoryNumber == 11:
        get_data.plus_products_from_product_model(11, "키보드")
    elif categoryNumber == 12:
        get_data.plus_products_from_product_model(12, "마우스")
    elif categoryNumber == 13:
        get_data.plus_products_from_product_model(13, "모니터")
    elif categoryNumber == 14:
        get_data.plus_products_from_product_model(14, "스피커")
        get_data.plus_products_from_product_model(14, "헤드셋")
    else:
        print("category23231")
        return render(request, 'category/error.html')


    outputDB = get_data.get_all_products(categoryNumber)

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

    # 결과를 렌더링하여 반환
    max_price_stat, min_price_stat, average_price_stat = calculate_price_stats(outputDB)

    return render(request, 'category/search_result.html', {'categoryName': categoryName, 'categoryNumber': categoryNumber, 'outputDB':outputDB, 'page_obj': page_obj, 'paginator':paginator, 'page_start_number':page_start_number,'page_end_number':page_end_number,'max_price_stat':max_price_stat, 'min_price_stat':min_price_stat, 'average_price_stat': average_price_stat})

def search_report_view(request):
    categoryNumber = request.GET.get('category', '')
    print("DD")
    categoryNumber = int(categoryNumber)
    categoryName = get_data.get_minorname(categoryNumber)

    sort = request.GET.get('sort', 'latest')
    aOption = request.GET.get('aoption', 'abcdef')

    print(aOption, "!1dd")


    min_price = request.GET.get('min', '0')
    max_price = request.GET.get('max', '3000000')

    if not min_price:
        min_price = '0'
    if not max_price:
        max_price = '3000000'

    if not sort :
        sort = 'lastest'

    if not sort and not min_price and not max_price:
        sort = 'dd'

    if aOption == "abcdef":
        sort = 'dd'

    print(sort)

    min_price = int(min_price)
    max_price = int(max_price)

    if  sort == 'latest':
        outputDB = get_data.get_products_by_latest(categoryNumber, min_price, max_price, aOption)
    elif sort == 'popularity':
        outputDB = get_data.get_products_by_popularity(categoryNumber, min_price, max_price, aOption)
    elif sort == 'price_low':
        print("adfafdaf")
        outputDB = get_data.get_products_by_price_low(categoryNumber, min_price, max_price, aOption)
    elif sort == 'price_high':
        outputDB = get_data.get_products_by_price_high(categoryNumber, min_price, max_price, aOption)
    else:
        outputDB = get_data.get_all_products(categoryNumber)
        print("카테앱 리포트 뷰 함수 error")

    paginator=Paginator(outputDB,48)
    print("22")
    
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
    save_search_history(request, categoryName)
    
    max_price_stat, min_price_stat, average_price_stat = calculate_price_stats(outputDB)
    return render(request, 'category/search_result.html', {'categoryName': categoryName, 'categoryNumber': categoryNumber, 'outputDB':outputDB, 'page_obj': page_obj, 'paginator':paginator, 'page_start_number':page_start_number,'page_end_number':page_end_number,'max_price_stat':max_price_stat, 'min_price_stat':min_price_stat, 'average_price_stat': average_price_stat})


def update_wishlist_status(request, page_obj):
    if request.user.is_authenticated:
        # 사용자의 위시리스트 가져옴
        wishlist = Wishlist.objects.get(user=request.user)
        # 위시리스트에 있는 상품의 ID 목록을 가져옴
        wishlist_product_ids = wishlist.products.values_list('Pd_IndexNumber', flat=True)

        for product in page_obj:
            product.is_in_wishlist = product.Pd_IndexNumber in wishlist_product_ids
    
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
