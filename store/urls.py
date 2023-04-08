from django.urls import path
from .views import *



app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='shop'),
    path("<int:product_id>/detail/", product_detail, name='detail'),
    path("new", new_product, name='new'),
    path("<int:product_id>/update", product_updat, name='update'),
    path("<int:product_id>/delete", product_delete, name='delete'),
    # comments
    path("<int:product_id>/comment/new", new_comment, name='comment_new'),
    path("<int:product_id>/comment/<int:comment_id>/delete", delete_comment, name='comment_delete'),
    #like button url
    path('like/', like_store, name='like-store'),
    path('like_store/', like_store_comment, name='like_comment'),
    # category
    path('<str:category_name>/category', CategoryView.as_view(), name='category'),
    # book


]

