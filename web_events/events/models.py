from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.

Author = settings.AUTH_USER_MODEL


class EventPostQuerySet(models.QuerySet):
    def eventtime(self):
        now = timezone.now()
        # Events.objects
        return self.filter(start_date__gte=now)  # this is a problem for my_events (Past, All)

    def search(self, query, category, start_event, end_event, time_range):
        lookup = (
                (Q(title__contains=query) |
                 Q(description__contains=query) |
                 Q(location__contains=query) |
                 Q(author__username=query) |
                 Q(event_type__contains=query) |
                 Q(host__contains=query)) &
                (Q(category=category[0]) |
                 Q(category=category[1])) &
                (Q(start_date__range=(time_range[0], time_range[1])) |
                 (Q(start_date__lte=start_event) &
                  Q(end_date__gte=end_event)))
        )
        return self.filter(lookup)

    def my_search(self, query, category, start_event, end_event, time_range):
        lookup = (
                (Q(title__contains=query) |
                 Q(description__contains=query) |
                 Q(location__contains=query) |
                 Q(author__username=query) |
                 Q(event_type__contains=query) |
                 Q(host__contains=query)) &
                (Q(category=category[0]) |
                 Q(category=category[1])) &
                (Q(start_date__range=(time_range[0], time_range[1])) |
                 (Q(start_date__lte=start_event) &
                  Q(end_date__gte=end_event)))

        )
        return self.filter(lookup)


class EventsPostManager(models.Manager):
    def get_queryset(self):
        return EventPostQuerySet(self.model, using=self._db)

    def eventtime(self):
        return self.get_queryset().eventtime()

    def search(self, query=None, category=None, start_event=None, end_event=None, time_range=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query, category, start_event, end_event, time_range)

    def my_search(self, query=None, category=None, start_event=None, end_event=None, time_range=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().my_search(query, category, start_event, end_event, time_range)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Events(models.Model):  # events_set -> queryset
    title = models.CharField(max_length=50, null=True)
    offline_online = (('offline event', 'offline event'), ('online event', 'online event'))
    event_type = models.CharField(
        max_length=20,
        choices=offline_online,
        default='offline'
    )
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    description = models.TextField(null=True)
    location = models.CharField(max_length=200, null=True)
    members_number = models.PositiveIntegerField(default=0)
    host = models.CharField(max_length=30, null=True)
    cover = models.ImageField(upload_to='./images/covers/', blank=True, null=True, default='./images/covers/fon.jpeg')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    author = models.ForeignKey(Author, default=1, on_delete=models.SET_NULL, null=True)  # SET_NULL
    join = models.ManyToManyField(User, related_name='join', blank=True)
    created = models.DateField(auto_now_add=True)

    objects = EventsPostManager()

    def __str__(self):
        return f'{self.title}'

    def total_members(self):
        return self.join.count()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    class Meta:
        ordering = ['start_date', 'start_time', 'end_date', 'end_time']



LIKE_CHOICES = (
    ('Join', 'Join'),
    ('UnJoin', 'UnJoin'),
)


class JoinModelButton(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Join', max_length=10)

    def __str__(self):
        return str(self.event)


class UserProfileInfoModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=30, default='qwqwqw12')
    profile_pic = models.ImageField(upload_to='./images/profile_pics', blank=True)

    def __str__(self):
        return self.user.username


class Comments(models.Model):
    event = models.ForeignKey(Events, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    text = models.TextField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created_date']
