from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from shipmate.contrib.models import UserLog
from shipmate.users.forms import UserAdminChangeForm, UserAdminCreationForm
from shipmate.users.models import Team, Role, Feature, OTPCode, FeatureLog, TeamLog, RoleLog

User = get_user_model()


class AccessUserInline(admin.TabularInline):
    model = User
    extra = 1
    fields = ['first_name', 'last_name', 'email']
    fk_name = 'access'


class UserLogInline(admin.TabularInline):
    model = UserLog
    extra = 0


class FeatureLogInline(admin.TabularInline):
    model = FeatureLog
    extra = 0


class TeamLogInline(admin.TabularInline):
    model = TeamLog
    extra = 0


class RoleLogInline(admin.TabularInline):
    model = RoleLog
    extra = 0


class IncludedFeaturesInline(admin.TabularInline):
    model = Role.included_features.through
    extra = 1


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    inlines = [UserLogInline]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "picture", "access", "team")}),
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
    inlines = [TeamLogInline]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    inlines = [AccessUserInline, RoleLogInline]


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    inlines = [FeatureLogInline]


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    ...
