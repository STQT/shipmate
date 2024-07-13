from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


def validate_positive(value):
    if value < 0:
        raise ValidationError('Price must be a positive number.')


class GoalGroup(models.Model):
    class Month(models.IntegerChoices):
        JANUARY = 1, 'January'
        FEBRUARY = 2, 'February'
        MARCH = 3, 'March'
        APRIL = 4, 'April'
        MAY = 5, 'May'
        JUNE = 6, 'June'
        JULY = 7, 'July'
        AUGUST = 8, 'August'
        SEPTEMBER = 9, 'September'
        OCTOBER = 10, 'October'
        NOVEMBER = 11, 'November'
        DECEMBER = 12, 'December'
    name = models.CharField(max_length=50)
    month = models.PositiveSmallIntegerField(choices=Month.choices, default=Month.JANUARY)


class Goal(models.Model):
    group = models.ForeignKey("GoalGroup", on_delete=models.CASCADE, related_name="goals")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="+")
    monthly = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[validate_positive])
    ave = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[validate_positive])

    def __str__(self):
        return f"#{self.pk} {self.group.name} | {self.group.get_month_display()}"
