from django.shortcuts import render
from .models import User, ProviderProfile
from django.db.models import Avg, Count
from reviews.models import Review
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

def providers_list(request):
    providers = User.objects.filter(role='provider')
    
    # We want to pass a list of enriched objects to the template
    # Since we don't have a direct ProviderProfile relation easily annotated in one query without complexity,
    # we'll build a list of dictionaries.
    
    provider_data = []
    for provider in providers:
        profile = ProviderProfile.objects.filter(user=provider).first()
        
        # Calculate stats
        reviews = Review.objects.filter(service__provider=provider)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0
        review_count = reviews.count()
        
        provider_data.append({
            'user': provider,
            'profile': profile,
            'avg_rating': round(avg_rating, 1),
            'review_count': review_count,
        })
        
    context = {
        'providers': provider_data
    }
    return render(request, 'users/providers_list.html', context)

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        location = request.POST.get('location')  # specifically capturing customer address
        role = request.POST.get('role', 'customer')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            location=location,
            role=role
        )

        if role == 'provider':
            ProviderProfile.objects.create(
                user=user,
                experience=request.POST.get('experience', 0),
                price=request.POST.get('price', 0.0)
            )

        messages.success(request, 'Registration successful. You can now login.')
        return redirect('login')

    return render(request, 'users/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')