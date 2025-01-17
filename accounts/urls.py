from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.sing_up_user, name="sing_up_user"),
    path('me/', views.current_user, name="current_user"),
    path('me/update', views.update_user, name="current_user"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path("reset_password/<str:token>/",
         views.reset_password, name="reset_password"),
]
