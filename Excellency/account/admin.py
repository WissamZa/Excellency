from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User

UserAdmin.add_fieldsets = (
    (
        None,
        {
            'classes': ('wide',),
            'fields': ('national_id', 'email', 'password1', 'password2'),
        },
    ),
)


admin.site.register(User, UserAdmin)
