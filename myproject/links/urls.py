from django.urls import path
from .views import FriendLinkListView
from .views import like_link
from .views import FriendLinkListView, like_link, increment_page_views

app_name = 'links'

urlpatterns = [
    path('like/<int:pk>/', like_link, name='like_link'),
    path('',FriendLinkListView.as_view(), name='index'),
    path('increment-views/', increment_page_views, name='increment_page_views'),

]