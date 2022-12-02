from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),

]
