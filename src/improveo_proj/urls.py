"""improveo_proj URL Configuration

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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from posts.views import PostCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('reports.urls', namespace='reports')),
    path('board/', include('posts.urls', namespace='posts')),
    path('messages/', include('user_messages.urls', namespace='messages')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('logout/', LogoutView.as_view(), name='logout'),
    # re_path(r"^.*$", PostCreateView.as_view(), name="main-redirect"),
]

# if settings.DEBUG:
#     urlpatterns = urlpatterns + \
#         static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns = urlpatterns + \
#         static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)
