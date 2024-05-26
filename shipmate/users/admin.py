from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from shipmate.users.forms import UserAdminChangeForm, UserAdminCreationForm
from shipmate.users.models import Team, Role, Feature, OTPCode

User = get_user_model()


class AccessUserInline(admin.TabularInline):
    model = User
    extra = 1
    fields = ['first_name', 'last_name', 'email']
    fk_name = 'access'


class IncludedFeaturesInline(admin.TabularInline):
    model = Role.included_features.through
    extra = 1


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "picture", "access")}),
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
    list_display = ["id", "email", "first_name", "last_name", "is_superuser"]
    search_fields = ["first_name", "last_name"]
    list_display_links = ["id", "email", "first_name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    ...


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    inlines = [AccessUserInline]


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    ...


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    ...
