from django.contrib import admin


# Register your models here.
from .models import *


admin.site.register(Events)
admin.site.register(Category)
admin.site.register(JoinModelButton)
admin.site.register(UserProfileInfoModel)
admin.site.register(Comments)






