"""
URL configuration for Flow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Custom 404 handler - Fix this line
def custom_404(request, exception):
    return render(request, '404.html', status=404)

# Change this line - remove 'flow.urls.' prefix
handler404 = custom_404  # or just 'custom_404'
# OR use the function directly
# handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('transactions.urls')),
    path('categories/', include('categories.urls')),
    path('goals/', include('goals.urls')),
]