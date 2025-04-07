from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('fetch-onu-data/', views.fetch_onu_data, name='fetch_onu_data'),
]