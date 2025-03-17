from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL pour l'administration de Django
    path('admin/', admin.site.urls),

    # Inclut les URLs de l'application 'plaintes'
    path('', include('plaintes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
