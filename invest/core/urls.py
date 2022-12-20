from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/send_investissement', views.send_investissement,
         name='send_investissement'),
    path('api/ipn', views.ipn,
         name='ipn'),
    path('api/success', views.success,
         name='success'),
    path('api/cancel', views.cancel,
         name='cancel'),
]
