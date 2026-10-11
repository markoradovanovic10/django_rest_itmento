
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from api.views import RegisterView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('admin/', admin.site.urls),
    path('', include('api.urls'))

]
