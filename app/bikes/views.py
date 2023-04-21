from django.shortcuts import render, get_object_or_404
from .models import Bike
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def bikes(request):
    """
     This function returns a paginated list of Bike objects ordered by
     creation date, along with distinct values for certain fields to
     enable search filters. It takes in a GET request object to determine
     the page number for the paginated results. The resulting data is
     rendered using a specified HTML template.
    """

    bikes = Bike.objects.order_by('-created_date')
    paginator = Paginator(bikes, 4)
    page = request.GET.get('page')
    paged_bikes = paginator.get_page(page)

    model_search = Bike.objects.values_list('model', flat=True).distinct()
    city_search = Bike.objects.values_list('city', flat=True).distinct()
    year_search = Bike.objects.values_list('year', flat=True).distinct()
    body_style_search = Bike.objects.values_list('body_style', flat=True).distinct()

    data = {
        'bikes': paged_bikes,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    return render(request, 'bikes/bikes.html', data)
