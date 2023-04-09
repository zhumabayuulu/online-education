
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from config.views import home

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', home, name='home'),
                  path('store/', include('store.urls')),
                  path('oku/', include('blog_oku.urls')),
                  path('chats/', include('chat.urls')),
                  path('blog_admin/', include('blog_admin.urls')),
                  path('blog_nature/', include('blog_nature.urls')),
                #path('accounts/', include('django.contrib.auth.urls')),
                  path('accounts/', include('accounts.urls')),
]
if settings.DEBUG:
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
