from django.urls import path

from TaskManager.common.views import NewsCreateView, comment_article, NewsDetailView, news_delete, NewsEditView

urlpatterns = [
    path('news-create/', NewsCreateView.as_view(), name='news create'),
    path('<int:pk>/article-comment/', comment_article, name='comment article'),
    path('<int:pk>/article-view/', NewsDetailView.as_view(), name='details article'),
    path('<int:pk>/article-edit/', NewsEditView.as_view(), name='edit article'),
    path('<int:pk>/article-delete/', news_delete, name='delete article'),
]
