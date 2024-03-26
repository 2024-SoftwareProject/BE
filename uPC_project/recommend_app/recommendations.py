from accounts_app.models import User, Wishlist, SearchHistory
from products_app.models import Product
import pandas as pd

# 특성 벡터 변환
from sklearn.feature_extraction.text import TfidfVectorizer

# KNN 모델 학습
from sklearn.neighbors import NearestNeighbors

# Create your views here.

# KNN(K-Nearest Neighbors)
# user-based Collaborative filtering
# 가중치 기준
# 1. SearcHistory의 keyword/search_time최신순
# 2. 사용자 별 Wishlist의 카테고리/마켓/가격/상품명 정보


# 사용자별 SearchHistory, Wishlist를 DataFrame으로 변환
def create_feature_dataframe():
    users = User.objects.all()
    data = []

    for user in users:
        # SearchHistory 기반 특성
        search_history = SearchHistory.objects.filter(user=user).order_by('search_time')[:10] # 사용자별 최근 10개 검색 기록
        keywords = ' '.join([sh.keyword for sh in search_history])

        # Wishlist 기반 특성
        wishlists = Wishlist.objects.filter(user=user)
        categories = []
        markets = []
        prices = []
        product_names = []

        for wishlist in wishlists:
            for product in wishlist.products.all():
                categories.append(product.Pd_Category)
                markets.append(product.Pd_Market)
                prices.append(str(product.Pd_Price))
                product_names.append(product.Pd_Name)

        categories = ' '.join(categories)
        markets = ' '.join(markets)
        prices = ' '.join(prices)
        product_names = ' '.join(product_names)

        data.append([user.id, keywords, categories, markets, prices, product_names])

    return pd.DataFrame(data, columns=['user_id', 'keywords', 'categories', 'markets', 'prices', 'product_names'])


# 텍스트 데이터를 TF-IDF 벡터로 변환
def transform_features_to_tfidf(df_features):
    vectorizer = TfidfVectorizer()
    combined_features = df_features['keywords']+ " " + df_features['categories'] + " " + df_features['markets'] + " " + df_features['product_names']
    tfidf_matrix = vectorizer.fit_transform(combined_features)
    return tfidf_matrix


# KNN 모델 학습
def train_knn_model(tfidf_matrix):
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=5, n_jobs=-1)
    model_knn.fit(tfidf_matrix)
    return model_knn


# 추천함수
def get_recommendations(user_id, model_knn, tfidf_matrix, df_features):
    user_idx = df_features.index[df_features['user_id']==user_id].tolist()[0]
    distances, indices = model_knn.kneighbors(tfidf_matrix[user_idx], n_neighbors=5)

    neighbor_indices = indices.flatten()[1:] # 자기 자신을 제외
    neighbor_user_ids = df_features.iloc[neighbor_indices]['user_id'].values

    recommended_products = Wishlist.objects.filter(user_id__in=neighbor_user_ids).exclude(user_id=user_id).values_list('products__Pd_IndexNumber', flat=True).distinct()
    products = Product.objects.filter(Pd_IndexNumber__in = recommended_products)
    return products