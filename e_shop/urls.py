from django.contrib import admin
from django.urls import path, include
from .utils.error_views import handler404_req, handler500_req
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('product.urls'))
]

handler404 = handler404_req
handler500 = handler500_req
