from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.diary_list, name='diary_list'),
    path('post_comment/<int:diary_id>/', views.post_comment, name='post_comment'),
    path('like/<int:diary_id>/', views.like_diary, name='like_diary'),
]