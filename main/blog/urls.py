"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/post/', include('post.api.urls', namespace='post')),
    path('api/comment/', include('comment.api.urls', namespace='comment')),
    path('api/favourite/', include('favourite.api.urls', namespace='favourite')),
    path('api/user/', include('account.api.urls', namespace='account')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# In order to check access token and refresh token validationi you can check it in cmd as follows.
# Access token 
# curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjIxMDIyNDk1LCJqdGkiOiI1MmI1M2QwNTk3Njg0NGM1ODQ1NWU4YWY1MDI0NmE5NCIsInVzZXJfaWQiOjJ9.Q60WCGWuDiEyezdexBoqcPGEDenGxmSxO8dgJa80lww" http://127.0.0.1:8000/api/favourite/list-create/
# Refresh token
# curl -X POST http://127.0.0.1:8000/api/token/refresh/ -d "refresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyMTEwODU3NSwianRpIjoiNWJmYWUwMjNiMzM1NDM2YTkzN2QzNWYzNTZjMzM1NjQiLCJ1c2VyX2lkIjoyfQ.H1N9MLaHccq5Dy3TUoDtbLf9U0rt-zDnb_5jsKlFKi8"
# When user reach api/token/ end point. It gives two token which encoded base64. Then Every access token has 5 min default expire time. In front end client can generate access token via using refresh token with api/token/refresh endpoint.
