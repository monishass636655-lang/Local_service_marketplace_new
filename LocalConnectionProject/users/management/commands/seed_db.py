import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User, ProviderProfile
from services.models import Category, Service
from bookings.models import Booking
from reviews.models import Review

class Command(BaseCommand):
    help = 'Seeds the database with 200 providers and related data for Karnataka.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Service.objects.all().delete()
        Category.objects.all().delete()
        ProviderProfile.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        locations = ['Bengaluru', 'Mysuru', 'Hubli', 'Mangaluru', 'Belagavi', 'Udupi', 'Shivamogga']
        categories_data = [
            'Home Cleaning', 'Plumbing Repair', 'Electrician', 'AC Servicing',
            'Appliance Sales', 'Electronics Repair', 'Carpentry', 'Pest Control',
            'Painting', 'Gardening', 'Car Washing', 'Beauty & Spa', 'Furniture Assembly',
            'Laptop Repair', 'Plumbing Maintenance', 'Electrical Sales', 'General Sales', 
            'Laundry Services', 'Home Security Setup', 'Deep Cleaning',
            'Milk Delivery', 'Newspaper Subscription', 'Grocery Delivery', 'Tiffin Service',
            'Pet Grooming', 'Home Tutor', 'Yoga Trainer', 'Solar Panel Sale', 'CCTV Sales'
        ]

        self.stdout.write('Creating Categories...')
        categories = []
        for cat_name in categories_data:
            cat = Category.objects.create(name=cat_name)
            categories.append(cat)

        self.stdout.write('Creating Customers...')
        customers = []
        for i in range(50):
            cust = User.objects.create_user(
                username=f'customer{i}',
                password='password123',
                first_name=f'Cust{i}',
                last_name='User',
                role='customer',
                phone=f'9{random.randint(100000000, 999999999)}',
                location=random.choice(locations)
            )
            customers.append(cust)

        self.stdout.write('Creating 200 Providers and Services...')
        providers = []
        services = []
        for i in range(1, 201):
            prov = User.objects.create_user(
                username=f'provider{i}',
                password='password123',
                first_name=f'Pro{i}',
                last_name='Expert',
                role='provider',
                phone=f'8{random.randint(100000000, 999999999)}',
                location=random.choice(locations)
            )
            
            # Provider Profile
            profile = ProviderProfile.objects.create(
                user=prov,
                experience=random.randint(1, 15),
                price=random.randint(200, 2000),
                is_verified=random.choice([True, True, True, False])
            )

            # Assign 1-3 random services to each provider
            prov_cats = random.sample(categories, k=random.randint(1, 3))
            for cat in prov_cats:
                svc = Service.objects.create(
                    provider=prov,
                    category=cat,
                    name=f'{cat.name} by {prov.first_name}',
                    description=f'Professional {cat.name} services offered with {profile.experience} years of experience. Satisfaction guaranteed.',
                    price=random.randint(300, 5000),
                    location=prov.location,
                )
                services.append(svc)
                profile.services.add(svc)
            
            providers.append(prov)

        self.stdout.write('Creating Bookings and Reviews...')
        
        statuses = ['pending', 'accepted', 'completed', 'cancelled']
        
        for _ in range(500):
            customer = random.choice(customers)
            service = random.choice(services)
            provider = service.provider

            # Booking
            status = random.choice(statuses)
            Booking.objects.create(
                customer=customer,
                provider=provider,
                service=service,
                date=timezone.now().date() + timezone.timedelta(days=random.randint(-30, 30)),
                time=timezone.now().time(),
                status=status
            )

            # Review (only if completed or just randomly)
            if status == 'completed' or random.random() > 0.5:
                Review.objects.create(
                    user=customer,
                    service=service,
                    rating=random.choices([1, 2, 3, 4, 5], weights=[5, 5, 10, 30, 50])[0],
                    comment=f'Service was {"excellent" if random.random() > 0.3 else "okay"}. Highly recommend for {service.category.name}.'
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))
