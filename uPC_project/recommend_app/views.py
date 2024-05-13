from django.shortcuts import render
from recommend_app.recommendations import create_feature_dataframe, transform_features_to_tfidf, train_knn_model
from recommend_app.recommendations import get_recommendations

# Create your views here.

def collaborative_filtering(user_id):
    df_features = create_feature_dataframe()
    tfidf_matrix = transform_features_to_tfidf(df_features)
    model_knn = train_knn_model(tfidf_matrix)
    recommended_products = get_recommendations(user_id, model_knn, tfidf_matrix, df_features)
    return recommended_products
 