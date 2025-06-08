# message/urls.py
from django.urls import path
from .views import CommentBoardView, AdminCommentView

# 添加这个命名空间声明 ↓
app_name = 'message'

urlpatterns = [
    path('', CommentBoardView.as_view(), name='comment_board'),
    path('admin/<uuid:comment_id>/', AdminCommentView.as_view(), name='admin_comment'),
]