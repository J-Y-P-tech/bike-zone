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


def search(request):
    """
    Gets all the data form model Bike and extracts the values for:
    model, city, year, body_style, transmission.
    Gets data from request and based on it searches the data from request
    and returns it filtered.
    """
    bikes = Bike.objects.order_by('-created_date')
    model_search = Bike.objects.values_list('model', flat=True).distinct()
    city_search = Bike.objects.values_list('city', flat=True).distinct()
    year_search = Bike.objects.values_list('year', flat=True).distinct()
    body_style_search = Bike.objects.values_list('body_style', flat=True).distinct()
    transmission_search = Bike.objects.values_list('transmission', flat=True).distinct()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            bikes = bikes.filter(description__icontains=keyword)

    if 'model' in request.GET:
        model = request.GET['model']
        if model:
            bikes = bikes.filter(model__iexact=model)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            bikes = bikes.filter(city__iexact=city)

    if 'year' in request.GET:
        year = request.GET['year']
        if year:
            bikes = bikes.filter(year__iexact=year)

    if 'body_style' in request.GET:
        body_style = request.GET['body_style']
        if body_style:
            bikes = bikes.filter(body_style__iexact=body_style)

    if 'transmission' in request.GET:
        transmission = request.GET['transmission']
        if transmission:
            bikes = bikes.filter(transmission__iexact=transmission)

    if 'min_price' in request.GET:
        min_price = request.GET['min_price']
        max_price = request.GET['max_price']
        if max_price:
            bikes = bikes.filter(price__gte=min_price, price__lte=max_price)

    data = {
        'bikes': bikes,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
        'transmission_search': transmission_search,
    }

    request.session.clear()

    return render(request, 'bikes/search.html', data)


def bike_detail(request, id):
    single_bike = get_object_or_404(Bike, pk=id)
    data = {
        'single_bike': single_bike,
    }
    return render(request, 'bikes/bike_detail.html', data)
