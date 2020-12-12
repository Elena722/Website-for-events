from rest_framework import serializers
from django.contrib.auth import get_user_model
from events.models import Events, Category, UserProfileInfoModel
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class EventsSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    # author = UserSerializer()
    class Meta:
        model = Events
        fields = ['id', 'title', 'event_type', 'start_date', 'end_date', 'start_time', 'end_time',
                  'description', 'location', 'coordinates_latitude', 'coordinates_longitude', 'host',
                  'cover', 'members_number', 'category']








