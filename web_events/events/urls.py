from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import create_event, event_post_update_view, event_post_delete_view
from .views import my_event_list, home_page_view, join_event, detail_event, members_list, register, add_comment
from .views import event_delete_comment, event_approve_comment, event_comment_update

# from .views import filter_category_page

# from . views import HomePageView

urlpatterns = [
    path('', home_page_view, name='home'),
    path('detail/<int:pk>', detail_event, name='event_detail'),
    path('create/', create_event, name='create_page'),
    path('detail/<int:pk>/edit', event_post_update_view, name='update_event_post'),
    path('detail/<int:pk>/delete', event_post_delete_view, name='delete_event_post'),
    path('filter/my_events/', my_event_list, name='my_list'),
    path('join/', join_event, name='join_event'),
    path('members/<int:pk>', members_list, name='members_list'),

    path('register/', register, name='registration'),
    path('detail/<int:pk>/add_comment', add_comment, name='add_comment'),
    path('detail/<int:pk>/delete_comment', event_delete_comment, name='comment_remove'),
    path('detail/<int:pk>/approve_comment', event_approve_comment, name='comment_approve'),
    path('detail/<int:pk>/edit_comment', event_comment_update, name='comment_update'),

    # path('filter_category/<str:category>/', filter_category_page, name='filter_category_page'),
    # path('filter/all/', views.EventListView.as_view(), name='list_view'),
    # path('events/', views.EventList.as_view(), name='events'),
    # path('create/', views.CreateEvent.as_view(), name='create_event'),
    # path('create/', views.CreateEventPage.as_view(), name="create_event_page"),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
