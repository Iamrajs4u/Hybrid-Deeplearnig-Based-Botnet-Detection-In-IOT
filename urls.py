from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Remote_User.urls')),
    path('serviceprovider/', include('Service_Provider.urls')),
]