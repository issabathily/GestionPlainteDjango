from django.contrib import admin

from .models import User ,Comment,Notification,AbstractUser,Report
# Register your models here.
admin.site.register(Comment)

admin.site.register(Report)