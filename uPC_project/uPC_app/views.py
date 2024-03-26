from django.shortcuts import render
from django.http import HttpResponse

from products_app.models import Product
from board_app.models import Post
from . import home_get_data
from recommend_app.recommendations import create_feature_dataframe, transform_features_to_tfidf, train_knn_model
from recommend_app.recommendations import get_recommendations

def home(request):
    popularity_outputDB = home_get_data.get_products_by_popularity()
    post_outputDB = home_get_data.get_posts()
    
    recommended_products = []
    if request.user.is_authenticated:
        df_features = create_feature_dataframe()
        tfidf_matrix = transform_features_to_tfidf(df_features)
        model_knn = train_knn_model(tfidf_matrix)
        recommended_products = get_recommendations(request.user.id, model_knn, tfidf_matrix, df_features)

    return render(request, 'home.html', {
        'popularity_outputDB':popularity_outputDB ,
        'post_outputDB': post_outputDB,
        'recommended_products':recommended_products})

