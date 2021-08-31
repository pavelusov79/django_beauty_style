"""django_beauty_style URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp import views
from mainapp.views import MainView, PortfolioView, ServicesView, NewsView, ContactsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cache_page(60*60)(MainView.as_view()), name='main'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('portfolio/', cache_page(60*60)(PortfolioView.as_view()), name='portfolio'),
    path('services/', cache_page(60*60)(ServicesView.as_view()), name='services'),
    path('news/', NewsView.as_view(), name='news'),
    path('ajax/load-masters/', views.load_masters, name='ajax_load_masters'),
    path('ajax/valid_fields/', views.valid_fields, name='valid_fields'),
    path('ajax/load_time/', views.load_time)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
