from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import CustomarProfile, LawyerProfile, User
from django.utils.translation import gettext_lazy as _


# class LawyerProfileInline(admin.StackedInline):
#    model = LawyerProfile
#    can_delete = False
#    verbose_name_plural = 'Profile'
#    fk_name = 'user'


class ProfileInline(admin.StackedInline):
   model = CustomarProfile
   if User.role == User.Lawyer:
      model = LawyerProfile
   can_delete = False
   verbose_name_plural = 'Profile'
   fk_name = 'user'


UserAdmin.inlines = (
    ProfileInline,
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
    (None, {"fields": ("username", "password")}),
    (_("Personal info"), {
     "fields": ("full_name", "email")}),
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
