from django.contrib import admin

from shipmate.insights.models import GoalGroup, Goal, LeadsInsight


@admin.register(GoalGroup)
class GoalGroupAdmin(admin.ModelAdmin):
    ...


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    ...


@admin.register(LeadsInsight)
class LeadsInsightAdmin(admin.ModelAdmin):
    ...
