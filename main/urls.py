from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/dashboard/', views.get_dashboard_updates, name='dashboard_updates'),
]

