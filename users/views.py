import json
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models  import Count
from .models import Users

def all_user(request):
    return HttpResponse('Returning all user')
def dashboard_view(request):
    return render(request, 'index.html')



logger = logging.getLogger(__name__)
def chart_view(request):
    event_by_year = Users.objects.exclude(start_year=None).values('start_year').annotate(num_events=Count('id'))
    likelihood_distribution = Users.objects.values('likelihood').annotate(num_events=Count('id'))

    years = [event['start_year'] for event in event_by_year]
    event_counts = [event['num_events'] for event in event_by_year]
    likelihood_values = [event['likelihood'] for event in likelihood_distribution]
    likelihood_counts = [event['num_events'] for event in likelihood_distribution]


    logger.debug('Years: %s', years)
    logger.debug('Event Counts: %s', event_counts)
    logger.debug('Likelihood Values: %s', likelihood_values)
    logger.debug('Likelihood Counts: %s', likelihood_counts)

    

    context = {
        'years': years,
        'event_counts': json.dumps(event_counts),
        'likelihood_values': json.dumps(likelihood_values),
        'likelihood_counts': json.dumps(likelihood_counts)
    }

    return render(request, 'index.html', context)
    


def region(request):


    events_by_region_year = Users.objects.values('region','start_year').annotate(num_events=Count('id'))
    region_year_data = {}

    for event in events_by_region_year:
        region = event['region']
        year = event['start_year']
        num_events = event['num_events']
        if region not in region_year_data:
            region_year_data[region] = {year: num_events}
        else:
            region_year_data[region][year] = num_events


    context = {
        'region_year_data': region_year_data
    }



    return render(request, 'region.html', context)
