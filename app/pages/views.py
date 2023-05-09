from django.shortcuts import render
from .models import Team
from bikes.models import Bike


def home(request):
    teams = Team.objects.all()
    featured_bikes = Bike.objects.order_by('-created_date').filter(is_featured=True)
    all_bikes = Bike.objects.order_by('-created_date')
    model_search = Bike.objects.values_list('model', flat=True).distinct()
    city_search = Bike.objects.values_list('city', flat=True).distinct()
    year_search = Bike.objects.values_list('year', flat=True).distinct()
    body_style_search = Bike.objects.values_list('body_style', flat=True).distinct()
    data = {
        'teams': teams,
        'featured_bikes': featured_bikes,
        'all_bikes': all_bikes,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    return render(request, 'pages/home.html', data)


def about(request):
    teams = Team.objects.all()
    data = {
        'teams': teams,
    }
    return render(request, 'pages/about.html', data)


def services(request):
    return render(request, 'pages/services.html')


def contact(request):
    return render(request, 'pages/contact.html')
