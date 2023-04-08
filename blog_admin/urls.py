from django.urls import path


from .views import (
    ArticleListView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleCreateView,
    like_postt,
    CategoryAdminView,
)

urlpatterns = [
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name="article_edit"),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    path('', ArticleListView.as_view(), name='adminn'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name="article_edit"),
    path('like/',like_postt , name='like-postt'),
    path('<str:admin_name>/category', CategoryAdminView.as_view(), name='admin_category'),

]