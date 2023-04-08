from django.urls import path
from .views import *
app_name = 'users'
urlpatterns = [
    path('register', SignupView.as_view(), name='register'),
    path("login/", Login.as_view(), name="login"),
    path('profile/<str:username>', ProfailView.as_view(), name='profile'),
    path('update/', UpdateProfileView.as_view(), name='update'),
    # saved product
    path('addremovesaved/<int:product_id>', AddRemoveSavedView.as_view(), name='addremovesaved'),
    path('saveds',SavedView.as_view(),name='saveds'),
    # saved nature
    path('savedsnature/<int:nature_id>', NatureSavedView.as_view(), name='naturesaved'),
    path('savedstest/<int:test_id>', TestSavedView.as_view(), name='test_saved'),
    path('savedsadmin/<int:admin_id>', AdminSavedView.as_view(), name='adminsaved'),
    path('savedslearn/<int:bloglearn_id>', LearnSavedView.as_view(), name='learnsaved'),
    path('recently_viewed',RecentlyViewedView.as_view(),name='recently_viewed'),
    path('logout/',logout_user,name='logout'),
    path('contact',contactForm,name='contact_form'),
    path('discover/', discover, name='discover'),

]
