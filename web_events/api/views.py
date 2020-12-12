from rest_framework import generics
from api.serializers import EventsSerializer, CategorySerializer, UserSerializer
from django.shortcuts import render, get_object_or_404
from events.models import Events, Category, UserProfileInfoModel
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS, IsAdminUser
from django.utils import timezone, dateformat
from rest_framework.decorators import api_view
from rest_framework import status


# Create your views here.

class UserPermissionsAll(permissions.BasePermission):
    """
    Owners of the object or admins can do anything.
    Everyone else can do nothing.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return False


class UserPermissionsObj(permissions.BasePermission):
    """
    Owners of the object or admins can do anything.
    Everyone else can do nothing.
    """

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.is_superuser:
            return True
        elif request.method == 'GET':
            return True
        return obj.author == request.user


class UserPermissionsObjPost(permissions.BasePermission):
    """
    Owners of the object or admins can do anything.
    Everyone else can do nothing.
    """

    def has_object_permission(self, request, view, obj):
        if request.user == obj.username or request.user.is_superuser:
            return True
        elif request.method == 'POST':
            return True
        return obj.username == request.user


class EventView(viewsets.ModelViewSet):
    '''Get list of future events'''
    queryset = Events.objects.eventtime()
    serializer_class = EventsSerializer
    permission_classes = (UserPermissionsAll, UserPermissionsObj)

    def get_queryset(self):
        period = self.request.query_params.get('period')
        now = dateformat.format(timezone.now(), 'Y-m-d')
        delta_three_month = dateformat.format(timezone.now() + timezone.timedelta(weeks=12), 'Y-m-d')
        delta_year = dateformat.format(timezone.now() + timezone.timedelta(weeks=52), 'Y-m-d')
        delta_negative_year = dateformat.format(timezone.now() - timezone.timedelta(weeks=52), 'Y-m-d')
        past_now = dateformat.format(timezone.now() - timezone.timedelta(days=1), 'Y-m-d')
        time_range = [now, delta_three_month]
        queryset = Events.objects.eventtime()

        if period == 'upcoming':  # for last entry
            start_event = now
            end_event = now
            time_range = [now, delta_three_month]
            queryset = (Events.objects.filter(start_date__range=(time_range[0], time_range[1])) or
                        Events.objects.filter(start_date__lte=start_event, end_date__gte=end_event)).order_by(
                'start_date')
        elif period == 'today':
            start_event = now
            end_event = now
            time_range = [now, now]
            queryset = (Events.objects.filter(start_date__range=(time_range[0], time_range[1])) or
                        Events.objects.filter(start_date__lte=start_event, end_date__gte=end_event)).order_by(
                'start_date')
        elif period == 'past':
            start_event = past_now
            end_event = past_now
            time_range = [delta_negative_year, past_now]
            queryset = (Events.objects.filter(start_date__range=(time_range[0], time_range[1])) or
                        Events.objects.filter(start_date__lte=start_event, end_date__lte=end_event)).order_by(
                'start_date')
        elif period == 'future':
            start_event = now
            end_event = now
            time_range = [now, delta_year]
            queryset = (Events.objects.filter(start_date__range=(time_range[0], time_range[1])) or
                        Events.objects.filter(start_date__lte=start_event, end_date__gte=end_event)).order_by(
                'start_date')
        elif period == 'all':
            start_event = now
            end_event = now
            time_range = [delta_negative_year, delta_year]
            queryset = (Events.objects.filter(start_date__range=(time_range[0], time_range[1])) or
                        Events.objects.filter(start_date__lte=start_event, end_date__gte=end_event)).order_by(
                'start_date')
        return queryset

    def create(self, validated_data):
        event = Events.objects.create(**validated_data)

        # for album_data in albums_data:
        #     Album.objects.create(artist=musician, **album_data)
        return event

# class CategoryView(viewsets.ModelViewSet):
#     '''Get list of future events'''
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]


# class UserView(viewsets.ModelViewSet):
#     '''Get list of future events'''
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (UserPermissionsObjPost,)


# class UserProfileView(viewsets.ModelViewSet):
#     '''Get list of future events'''
#     queryset = UserProfileInfoModel.objects.all()
#     serializer_class = UserProfileSerializer


class MyEventsView(generics.ListAPIView):
    '''Get list of my future events'''
    serializer_class = EventsSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Events.objects.filter(author__username=username)
