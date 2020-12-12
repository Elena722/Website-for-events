from rest_framework import routers
from django.urls import path, include
from .views import EventView, MyEventsView

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'events', EventView)
# router.register(r'category', CategoryView)
# router.register(r'users', UserView)
# router.register(r'users_profile', UserProfileView)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('my_events/<username>', MyEventsView.as_view()),
]
