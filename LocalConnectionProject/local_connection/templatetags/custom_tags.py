from django import template
import random

register = template.Library()

# Dictionary mapping category names to contextual Unsplash images
CATEGORY_IMAGES = {
    'Home Cleaning': [
        'https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=400&q=80',
        'https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=400&q=80',
    ],
    'Plumbing Repair': [
        'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=400&q=80',
        'https://images.unsplash.com/photo-1542013936693-884638332954?auto=format&fit=crop&w=400&q=80',
    ],
    'Plumbing Maintenance': [
        'https://images.unsplash.com/photo-1514126516501-e71e7f8e8e42?auto=format&fit=crop&w=400&q=80',
    ],
    'Electrician': [
        'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=400&q=80',
        'https://images.unsplash.com/photo-1555963966-b7ae5404b6ed?auto=format&fit=crop&w=400&q=80',
    ],
    'Electrical Sales': [
        'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=400&q=80',
    ],
    'AC Servicing': [
        'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?auto=format&fit=crop&w=400&q=80',
    ],
    'Appliance Sales': [
        'https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?auto=format&fit=crop&w=400&q=80',
        'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=400&q=80',
    ],
    'Electronics Repair': [
        'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=400&q=80',
        'https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=400&q=80',
    ],
    'Laptop Repair': [
        'https://images.unsplash.com/photo-1588508065123-287b28e013da?auto=format&fit=crop&w=400&q=80',
        'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=400&q=80',
    ],
    'Carpentry': [
        'https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=400&q=80',
    ],
    'Furniture Assembly': [
        'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=400&q=80',
    ],
    'Pest Control': [
        'https://images.unsplash.com/photo-1518152006812-edab29b069ac?auto=format&fit=crop&w=400&q=80',
    ],
    'Painting': [
        'https://images.unsplash.com/photo-1562259929-b4e1fd3aef09?auto=format&fit=crop&w=400&q=80',
    ],
    'Gardening': [
        'https://images.unsplash.com/photo-1416879598555-dfff7dbfd622?auto=format&fit=crop&w=400&q=80',
    ],
    'Deep Cleaning': [
        'https://images.unsplash.com/photo-1563453392212-326f5e854473?auto=format&fit=crop&w=400&q=80',
    ],
    'Car Washing': [
        'https://images.unsplash.com/photo-1507136566006-cfc505b114fc?auto=format&fit=crop&w=400&q=80',
    ],
    'Beauty & Spa': [
        'https://images.unsplash.com/photo-1540555700478-4be289aef09a?auto=format&fit=crop&w=400&q=80',
    ],
    'Laundry Services': [
        'https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?auto=format&fit=crop&w=400&q=80',
        'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=400&q=80',
    ],
    'General Sales': [
        'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=400&q=80',
    ],
    'Home Security Setup': [
        'https://images.unsplash.com/photo-1558002038-1055907df827?auto=format&fit=crop&w=400&q=80',
    ],
    'CCTV Sales': [
        'https://images.unsplash.com/photo-1521618755572-156ae0cdd74d?auto=format&fit=crop&w=400&q=80',
    ],
    'Solar Panel Sale': [
        'https://images.unsplash.com/photo-1509391366360-2e959784a276?auto=format&fit=crop&w=400&q=80',
    ],
    'Grocery Delivery': [
        'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=400&q=80',
    ],
    'Milk Delivery': [
        'https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=400&q=80',
    ],
    'Tiffin Service': [
        'https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=400&q=80',
    ],
    'Newspaper Subscription': [
        'https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=400&q=80',
    ],
    'Pet Grooming': [
        'https://images.unsplash.com/photo-1587300003388-59208cc962cb?auto=format&fit=crop&w=400&q=80',
    ],
    'Home Tutor': [
        'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=400&q=80',
    ],
    'Yoga Trainer': [
        'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=400&q=80',
    ],
}

DEFAULT_IMAGE = 'https://images.unsplash.com/photo-1556761175-5973e8a7c293?auto=format&fit=crop&w=400&q=80'


@register.simple_tag
def context_image(category_name, seed=None):
    """Returns a contextual image URL based on the category name."""
    images = CATEGORY_IMAGES.get(category_name)
    if not images:
        return DEFAULT_IMAGE
    if seed is not None:
        idx = hash(seed) % len(images)
        return images[idx]
    return random.choice(images)


@register.simple_tag
def provider_image(provider, seed=None):
    """Returns a contextual image URL based on the provider's first service category."""
    from services.models import Service
    first_service = Service.objects.filter(provider=provider).first()
    if first_service:
        category_name = first_service.category.name
        images = CATEGORY_IMAGES.get(category_name)
        if images:
            if seed is not None:
                idx = hash(seed) % len(images)
                return images[idx]
            return random.choice(images)
    return DEFAULT_IMAGE
