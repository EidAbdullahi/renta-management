from django.urls import path
from . import views

urlpatterns = [
   
    path('hotels/', views.hotel_search, name='hotel_search'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('reservation/success/', views.reservation_success, name='reservation_success'),
]


