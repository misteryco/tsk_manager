from django.urls import path

from TaskManager.common.views import NewsCreateView, comment_article

urlpatterns = [
    path('news-create/', NewsCreateView.as_view(), name='news create'),
    path('<int:pk>/article-comment/', comment_article, name='comment article'),
]
