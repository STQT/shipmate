import django_filters
from django.contrib.auth import get_user_model
from shipmate.users.models import Team, Role

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = User
        fields = ['is_active']


class TeamFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Team.TeamStatusChoices.choices)

    class Meta:
        model = Team
        fields = ['status']


class RoleFilter(django_filters.FilterSet):
    access_status = django_filters.ChoiceFilter(choices=Role.RoleAccessStatusChoices.choices)

    class Meta:
        model = Role
        fields = ['access_status']
