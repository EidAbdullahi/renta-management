from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('create_project/', views.create_project, name='create_project'),
    path('create_unit/', views.create_unit, name='create_unit'),
    path('projects/<int:project_id>/units/', views.view_units, name='view_units'),
    path('unit/<int:unit_id>/book/', views.book_unit, name='book_unit'),
    path('booking/<int:booking_id>/', views.booking_details, name='booking_details'),
    path('booking/<int:booking_id>/add_payment/', views.add_payment, name='add_payment'),
    path('booked_units/', views.booked_units, name='booked_units'),
]
