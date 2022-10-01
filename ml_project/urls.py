from django.urls import path
from . import views

app_name='ml_project'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('recommend_data', views.recommend_data, name='recommend_data'),
]