from django.shortcuts import render
from .models import SearchQuery
from events.models import *
from django.utils import timezone, dateformat


# from events.filters import EventsFilter


# Create your views here.

def search_view(request):
    template_name = 'searches/view.html'
    query = request.GET.get('q', None)
    _category = request.GET.get('qq', None)
    _start_date = request.GET.get('qqq', None)
    now = dateformat.format(timezone.now(), 'Y-m-d')
    delta_three_month = dateformat.format(timezone.now() + timezone.timedelta(weeks=12), 'Y-m-d')
    delta_year = dateformat.format(timezone.now() + timezone.timedelta(weeks=52), 'Y-m-d')
    delta_negative_year = dateformat.format(timezone.now() - timezone.timedelta(weeks=52), 'Y-m-d')
    past_now = dateformat.format(timezone.now() - timezone.timedelta(days=1), 'Y-m-d')
    if _start_date == 'Today':
        start_date = [now, now]
    elif _start_date == 'Upcoming':
        start_date = [now, delta_three_month]
    elif _start_date == 'Future':
        start_date = [now, delta_year]
    elif _start_date == 'Past':
        start_date = [delta_negative_year, past_now]
    elif _start_date == 'All':
        start_date = [delta_negative_year, delta_year]
    if _category == 'Party':
        category = [1, None]
    elif _category == 'Film':
        category = [2, None]
    elif _category == 'All':
        category = [1, 2]
    author = None
    if request.user.is_authenticated:
        author = request.user
    context = {'query': query, 'category': _category, 'start_date': _start_date}
    SearchQuery.objects.create(author=author, query=query)
    events = Events.objects.search(query=query, category=category, start_date=start_date)
    context['events'] = events
    return render(request, template_name, context)

def my_search_view(request):
    template_name = 'searches/view.html'
    query = request.GET.get('q', None)
    _category = request.GET.get('qq', None)
    _start_date = request.GET.get('qqq', None)
    _role = request.GET.get('qqqq', None)
    now = dateformat.format(timezone.now(), 'Y-m-d')
    delta_three_month = dateformat.format(timezone.now() + timezone.timedelta(weeks=12), 'Y-m-d')
    delta_year = dateformat.format(timezone.now() + timezone.timedelta(weeks=52), 'Y-m-d')
    delta_negative_year = dateformat.format(timezone.now() - timezone.timedelta(weeks=52), 'Y-m-d')
    past_now = dateformat.format(timezone.now() - timezone.timedelta(days=1), 'Y-m-d')
    events2 = []
    events = []
    if _start_date == 'Today':
        start_date = [now, now]
    elif _start_date == 'Upcoming':
        start_date = [now, delta_three_month]
    elif _start_date == 'Future':
        start_date = [now, delta_year]
    elif _start_date == 'Past':
        start_date = [delta_negative_year, past_now]
    elif _start_date == 'All':
        start_date = [delta_negative_year, delta_year]
    if _category == 'Party':
        category = [1, None]
    elif _category == 'Film':
        category = [2, None]
    elif _category == 'All':
        category = [1, 2]
    if _role == 'Organizer':
        events = Events.objects.filter(author=request.user)
    elif _role == 'Participant':
        events = Events.objects.none()
        events2 = JoinModelButton.objects.filter(user=request.user, value='Join')
    elif _role == 'All':
        events = Events.objects.filter(author=request.user)
        events2 = JoinModelButton.objects.filter(user=request.user, value='Join')
    print(type(events))
    author = request.user
    context = {'query': query, 'category': _category, 'start_date': _start_date, 'role':_role}
    SearchQuery.objects.create(author=author, query=query)
    for event in events2:
        obj = Events.objects.filter(title=event)
        events = events | obj
    events = events.my_search(query=query, category=category, start_date=start_date)
    context['events'] = events
    return render(request, template_name, context)
