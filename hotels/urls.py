from django.urls import path
from . import views

urlpatterns = [
    path('hotels/', views.hotel_search, name='hotel_search'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('book/<int:room_type_id>/', views.book_room_type, name='book_room'),  # updated here
    path('reservation/success/', views.reservation_success, name='reservation_success'),
    path('reservation/receipt/<int:reservation_id>/', views.reservation_receipt, name='reservation_receipt'),
    path('hotel-dashboard/', views.dashboard_view, name='hotel_dashboard'),
    path('reservation/<int:reservation_id>/success/', views.mark_successful, name='mark_successful'),
    path('reservation/<int:reservation_id>/unsuccess/', views.mark_unsuccessful, name='mark_unsuccessful'),
]
