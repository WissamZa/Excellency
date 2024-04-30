from django.contrib import admin
from .models import Service,Rating

admin.site.register(Service)

# Register your models here.
admin.site.register(Rating)