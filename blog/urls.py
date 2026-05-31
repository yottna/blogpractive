# blog/urls.py (앱 안의 URL 설정 파일)
from django.urls import path
from .views import BlogListView, BlogDetailView, CommentListView

urlpatterns = [
    # 기존 'blogs/' 에서 앞부분을 비워서 '' 로 수정합니다.
    path('', BlogListView.as_view(), name='blog-list'), 
    path('<int:blog_id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('<int:blog_id>/comments/', CommentListView.as_view(), name='comment-list'),
]