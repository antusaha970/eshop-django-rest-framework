from django.urls import path
from . import views
urlpatterns = [
    path("orders/new/", views.make_order),
    path("orders/", views.get_all_orders),
    path("orders/<str:pk>/", views.get_single_order),
    path("orders/<str:pk>/update", views.update_order),
    path("orders/<str:pk>/delete", views.delete_order),
]
