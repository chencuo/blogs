from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='index'),
    path('<slug:slug>/', views.ArticleDetailView.as_view(), name='detail'),
]