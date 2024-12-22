from django.contrib import admin

from advertisement.models import Advertisement


# Register your models here.
@admin.register(Advertisement)
class AdvertiseAdmin(admin.ModelAdmin):
    pass