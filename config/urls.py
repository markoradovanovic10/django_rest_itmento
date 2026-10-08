
from django.contrib import admin
from django.urls import path
from api.views import test_enpoint

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test_enpoint, name='test_endpoint')
]
