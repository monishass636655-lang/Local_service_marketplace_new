from django.shortcuts import render
from django.db.models import Count, Avg
from services.models import Category, Service
from users.models import User, ProviderProfile
from bookings.models import Booking
from reviews.models import Review

def home(request):
    # Quick stats
    total_providers = User.objects.filter(role='provider').count()
    live_requests = Booking.objects.filter(status='pending').count()
    total_bookings = Booking.objects.count()

    # If no data, render empty placeholders so it doesn't crash before seeding
    if total_providers == 0:
        return render(request, 'dashboard.html', {
            'total_providers': 0, 'live_requests': 0, 'total_bookings': 0,
            'categories': [], 'top_providers': [], 'recent_bookings': [], 'recent_reviews': []
        })

    # Categories with count of services
    categories = Category.objects.annotate(service_count=Count('service')).order_by('-service_count')[:6]
    
    # Top Providers
    top_providers = ProviderProfile.objects.filter(is_verified=True).order_by('-experience')[:6]
    for profile in top_providers:
        reviews = Review.objects.filter(service__provider=profile.user)
        avg = reviews.aggregate(Avg('rating'))['rating__avg']
        profile.avg_rating = round(avg, 1) if avg else 4.5
        profile.review_count = reviews.count()
    
    # Recent Bookings (Requests)
    recent_bookings = Booking.objects.order_by('-id')[:6]
    
    # Recent Reviews
    recent_reviews = Review.objects.order_by('-created_at')[:6]

    context = {
        'total_providers': total_providers,
        'live_requests': live_requests,
        'total_bookings': total_bookings,
        'categories': categories,
        'top_providers': top_providers,
        'recent_bookings': recent_bookings,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'dashboard.html', context)