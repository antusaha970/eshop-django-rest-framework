from django.contrib import admin
from django.urls import path, include
from .utils.error_views import handler404_req, handler500_req
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('product.urls')),
    path('api/', include('accounts.urls')),
    path("api/token/", TokenObtainPairView.as_view(), name="obtain_token")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = handler404_req
handler500 = handler500_req
