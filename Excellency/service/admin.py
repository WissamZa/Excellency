from django.contrib import admin

from .models import Service, Rating, Comment


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['subject', 'lawyer', 'customar', 'order_type', 'status']
    list_filter = ['created_date']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'added_date']
    list_filter = ['added_date']


admin.site.register(Service, ServiceAdmin)

admin.site.register(Comment, CommentAdmin)

# Register your models here.
admin.site.register(Rating)
