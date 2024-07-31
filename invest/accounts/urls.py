from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path("out", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path('change_password',  views.change_password, name='change_password'),
    path("hx/change_profile", views.hx_update_user_profile_img,
         name="change_profile"),
    path("hx/change_carte", views.hx_update_user_carte_img, name="change_carte"),
]
