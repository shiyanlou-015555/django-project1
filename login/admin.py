from django.contrib import admin

# Register your models here.
from . import models

#对接你的模型
admin.site.register(models.User)
admin.site.register(models.ConfirmString)