from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.sing_up_user, name="sing_up_user"),
    path('me/', views.current_user, name="current_user"),
]
