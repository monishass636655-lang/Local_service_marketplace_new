from django.urls import path
from . import views

urlpatterns = [
    path('provider/', views.provider_dashboard, name='provider_dashboard'),
    path('my-bookings/', views.customer_dashboard, name='customer_dashboard'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('accept/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('complete/<int:booking_id>/', views.complete_booking, name='complete_booking'),
    path('payment/<int:booking_id>/', views.process_payment, name='process_payment'),
]