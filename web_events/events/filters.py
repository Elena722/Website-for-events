import django_filters

from .models import *

class EventsFilter(django_filters.FilterSet):
    class Meta:
        model = Events
        fields = ['start_date']