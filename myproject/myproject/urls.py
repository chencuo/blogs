"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path,include
from home.views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name = 'home'),
    path('articles/', include('articles.urls',)),
     path('search/', include('search.urls')),
    path('links/', include('links.urls')),
    path('message/', include(('message.urls', 'message'), namespace='message')),
    path('diary/', include('diary.urls')),
    path('about/', include('about.urls')),
]

# 开发环境提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)