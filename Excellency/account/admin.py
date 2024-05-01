from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import CustomarProfile, LawyerProfile, User
from django.utils.translation import gettext_lazy as _


class CProfileInline(admin.StackedInline):
    model = CustomarProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class LProfileInline(admin.StackedInline):
    model = LawyerProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(UserAdmin):
    model = User
    list_display = ['full_name', 'email', 'get_certified', 'role']

    def get_certified(self, obj):
        return obj.lawyer_profile.certified


# UserAdmin.list_display = 'full_name', 'email', 'lawyer', 'role'


UserAdmin.inlines = (
    CProfileInline, LProfileInline,
)
UserAdmin.add_fieldsets = (
    (
        None,
        {
            'classes': ('wide',),
            'fields': ('full_name', 'national_id', 'email', 'role', 'password1', 'password2'),

        },
    ),
)

UserAdmin.fieldsets = (
    (None, {"fields": ("password",)}),
    (_("Personal info"), {
     "fields": ("full_name", 'national_id', 'role', "email")}),
    (
        _("Permissions"),
        {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        },
    ),
    (_("Important dates"), {"fields": ("last_login", "date_joined")}),
)
admin.site.register(User, UserAdmin)
