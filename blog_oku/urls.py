from django.urls import path
from .views import *


app_name = 'okuu'
urlpatterns = [

    path('',BlogView.as_view(),name='learn_view'),
    path('new/', OkuCreateView.as_view(), name='oku_new'),
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name="article_edit"),
    path("<int:bloglearn_id>/delete", blog_learn_delete, name='bloglearn_delete'),
    path("<int:bloglearn_id>/detail", BlogDetail.as_view(), name='learn_detail'),
    # comments url
    path("<int:bloglearn_id>/comment/new", learn_comment, name='blog_comment_new'),
    path("<int:bloglearn_id>/comment/<int:comment_id>/delete", delete_learn_comment, name='comment_delete'),
    # end comments url
    # test url
    path('list/',testlist,name='list_test'),
    path('<int:test_id>/ready_to_test',ready_to_test,name="ready_to_test"),
    path('<int:test_id>/test',test,name="test"),
    path('<int:checktest_id>/checktest',checktest,name='checktest'),
    path('new_test',new_test,name='new_test'),
    path('<int:test_id>/new_question',new_question,name='new_question'),
    # category url
    path('<str:oku_name>/category', CategoryLearnView.as_view(), name='oku_category'),
    path('test/<str:category_name>/category', TestView.as_view(), name='category'),
    # end category
    # like button url
    path('like/', like_oku, name='like-oku'),
    path('like/', like_learn_detail, name='like-detail'),
    path('like_test/', like_test, name='like-test'),
    path('like_liki/', like_learn_comment, name='like_learn_comment'),
    # end like button url
]