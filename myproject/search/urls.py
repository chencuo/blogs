# search/urls.py

from django.urls import path
from . import views  # 导入您的视图函数

urlpatterns = [
    path('', views.search_view, name='search'),
]