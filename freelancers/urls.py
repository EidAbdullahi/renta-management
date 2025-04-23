from django.urls import path
from . import views

urlpatterns = [
    path('', views.freelancer_list, name='freelancer_list'),
    path('freelancer/<int:pk>/', views.freelancer_detail, name='freelancer_detail'),
    
]
