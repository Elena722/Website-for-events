from django.contrib import admin

# Register your models here.
from .models import *

# order inside admin panel
class JoinModelButtonAdmin(admin.ModelAdmin):
    fields = ['user', 'value', 'event']
    # list_filter = ['value']
    # list_display = ['value']
    # list_editable = ['value']  # list_display

class CommentsAdmin(admin.ModelAdmin):
    fields = ['event', 'text', 'author', 'created_date', 'approved_comment']

# search inside admin panel
class EventsAdmin(admin.ModelAdmin):
    search_fields = ['title']
    # list_filter = ['author', 'category']
    # list_display = ['id', 'title', 'author']

admin.site.register(Events, EventsAdmin)
admin.site.register(Category)
admin.site.register(JoinModelButton, JoinModelButtonAdmin)
admin.site.register(UserProfileInfoModel)
admin.site.register(Comments, CommentsAdmin)






