from django.urls import path


from .views import *
app_name = 'nature'
urlpatterns = [

    path('', NatureView, name='nature'),
    path('new', NatureCreateView.as_view(), name='new'),
    path("<int:product_id>/delete", nature_delete, name='delete'),
    path("<int:nature_id>/update", nature_update, name='update'),

    path('<str:nature_name>/category', CategoryNatureView.as_view(), name='nature_category'),
    path('like/',like_post , name='like-post')
    ]