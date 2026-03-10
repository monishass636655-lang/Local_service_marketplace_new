from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Booking, Notification
from services.models import Service
from users.models import User
from django.utils import timezone
import datetime
import json
import hmac
import hashlib
import urllib.request
import urllib.parse
import base64

# Razorpay test credentials (replace with live keys for production)
RAZORPAY_KEY_ID = 'rzp_test_YouTestKeyHere'
RAZORPAY_KEY_SECRET = 'YourTestSecretHere'

@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        
        # Simple validation
        if date_str and time_str:
            if True: # Kept for indentation
                customer = request.user

            booking = Booking.objects.create(
                customer=customer,
                provider=service.provider,
                service=service,
                date=date_str,
                time=time_str,
                status='pending'
            )
            # Notify Customer
            Notification.objects.create(
                user=customer,
                message=f'You have booked {service.name} for {date_str} at {time_str}.',
                booking=booking,
                notification_type='booking_created'
            )
            # Notify Provider
            Notification.objects.create(
                user=service.provider,
                message=f'New booking request from {customer.first_name} for {service.name}.',
                booking=booking,
                notification_type='booking_created'
            )
            messages.success(request, f'Successfully booked {service.name}!')
            return redirect('home')
            
    return redirect('service_detail', id=service.id)

@login_required
def provider_dashboard(request):
    provider = request.user
    
    bookings = Booking.objects.filter(provider=provider).order_by('-date', '-time')
    
    notifications = Notification.objects.filter(user=provider).order_by('-created_at')[:10]
    
    context = {
        'provider': provider,
        'bookings': bookings,
        'notifications': notifications,
    }
    return render(request, 'bookings/provider_dashboard.html', context)

@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.status = 'accepted'
        booking.save()
        # Notify Customer
        Notification.objects.create(
            user=booking.customer,
            message=f'Expert {booking.provider.first_name} has accepted your booking for {booking.service.name}.',
            booking=booking,
            notification_type='booking_accepted'
        )
        messages.success(request, 'Booking accepted!')
    return redirect('provider_dashboard')

@login_required
def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.status = 'completed'
        booking.save()
        # Notify Customer
        Notification.objects.create(
            user=booking.customer,
            message=f'Your service "{booking.service.name}" has been marked as completed by the expert.',
            booking=booking,
            notification_type='booking_completed'
        )
        messages.success(request, 'Booking marked as completed!')
    return redirect('provider_dashboard')

@login_required
def customer_dashboard(request):
    customer = request.user
    
    # Filter bookings by the logged-in user
    bookings = Booking.objects.filter(customer=customer).order_by('-date', '-time')
    
    notifications = Notification.objects.filter(user=customer).order_by('-created_at')[:10]
    
    context = {
        'customer': customer,
        'bookings': bookings,
        'notifications': notifications,
    }
    return render(request, 'bookings/customer_dashboard.html', context)

@login_required
def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if request.method == 'POST':
        # Mock payment processing
        booking.payment_status = 'paid'
        booking.save()
        # Notify Customer
        Notification.objects.create(
            user=booking.customer,
            message=f'Payment of ${booking.service.price} for {booking.service.name} was successful!',
            booking=booking,
            notification_type='payment_success'
        )
        # Notify Provider
        Notification.objects.create(
            user=booking.provider,
            message=f'Payment received: ${booking.service.price} from {booking.customer.first_name} for {booking.service.name}.',
            booking=booking,
            notification_type='payment_success'
        )
        messages.success(request, f'Payment for {booking.service.name} successful!')
    return redirect('customer_dashboard')


@login_required
def create_razorpay_order(request, booking_id):
    """Create a Razorpay order for online payment."""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if booking.payment_status == 'paid':
        messages.info(request, 'This booking is already paid.')
        return redirect('customer_dashboard')

    # Amount in paise (INR smallest unit). e.g., ₹500 = 50000 paise
    amount_paise = int(float(booking.service.price) * 100)

    # Build Razorpay order via their REST API using Python stdlib
    razorpay_url = 'https://api.razorpay.com/v1/orders'
    payload = json.dumps({
        'amount': amount_paise,
        'currency': 'INR',
        'receipt': f'booking_{booking.id}',
    }).encode('utf-8')

    credentials = f'{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}'
    encoded_creds = base64.b64encode(credentials.encode()).decode()

    req = urllib.request.Request(
        razorpay_url,
        data=payload,
        headers={
            'Authorization': f'Basic {encoded_creds}',
            'Content-Type': 'application/json',
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req) as resp:
            order_data = json.loads(resp.read().decode())
        context = {
            'booking': booking,
            'razorpay_order_id': order_data['id'],
            'razorpay_key_id': RAZORPAY_KEY_ID,
            'amount_paise': amount_paise,
            'currency': 'INR',
        }
        return render(request, 'bookings/razorpay_checkout.html', context)
    except Exception as e:
        # Razorpay API unavailable — fall back to mock payment page
        messages.warning(request, 'Online payment gateway is in test mode. Using simulated payment.')
        context = {
            'booking': booking,
            'razorpay_order_id': f'order_demo_{booking.id}',
            'razorpay_key_id': RAZORPAY_KEY_ID,
            'amount_paise': amount_paise,
            'currency': 'INR',
            'demo_mode': True,
        }
        return render(request, 'bookings/razorpay_checkout.html', context)


@csrf_exempt
def verify_razorpay_payment(request):
    """Verify Razorpay payment signature and mark booking as paid."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    data = json.loads(request.body)
    razorpay_order_id = data.get('razorpay_order_id', '')
    razorpay_payment_id = data.get('razorpay_payment_id', '')
    razorpay_signature = data.get('razorpay_signature', '')
    booking_id = data.get('booking_id')

    # HMAC-SHA256 signature verification
    expected_signature = hmac.new(
        RAZORPAY_KEY_SECRET.encode(),
        f'{razorpay_order_id}|{razorpay_payment_id}'.encode(),
        hashlib.sha256
    ).hexdigest()

    booking = get_object_or_404(Booking, id=booking_id)

    # In demo mode, skip signature check
    is_demo = razorpay_order_id.startswith('order_demo_')
    if is_demo or expected_signature == razorpay_signature:
        booking.payment_status = 'paid'
        booking.save()
        Notification.objects.create(
            user=booking.customer,
            message=f'✅ Online payment of ₹{booking.service.price} for "{booking.service.name}" was successful!',
            booking=booking,
            notification_type='payment_success'
        )
        Notification.objects.create(
            user=booking.provider,
            message=f'💰 Payment of ₹{booking.service.price} received from {booking.customer.first_name} for "{booking.service.name}".',
            booking=booking,
            notification_type='payment_success'
        )
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=400)
