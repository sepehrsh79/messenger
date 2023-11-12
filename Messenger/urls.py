from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from Messenger import settings
from chat.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('chat/', include('chat.urls')),
    path('account/', include('account.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
