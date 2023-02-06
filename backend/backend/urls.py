from django.contrib import admin
from django.urls import include, path
from api import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(urls))
]
