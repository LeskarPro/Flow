from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)


handler404 = custom_404
handler500 = custom_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),
    path('', include('transactions.urls')),
    path('categories/', include('categories.urls')),
    path('goals/', include('goals.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
