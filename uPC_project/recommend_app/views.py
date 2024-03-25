from django.shortcuts import render

from django.db.models import Q
from accounts_app.models import User, Wishlist
from products_app.models import Product
import numpy as np

# Create your views here.

# KNN(K-Nearest Neighbors)
# user-based Collaborative filltering
# 가중치 기준
# 1. 검색 키워드
# 2. 사용자 위시의 카테고리/마켓/가격/상품명 정보 

