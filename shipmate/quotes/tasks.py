from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from shipmate.quotes.models import Quote, QuoteStatusChoices, QuoteDates


@shared_task
def follow_up_quotes():
    # Get the current date and time
    now = timezone.now()
    # Calculate the date 7 days ago
    seven_days_ago = now - timedelta(days=7)

    # Find all quotes with status 'Quote' and quoted more than 7 days ago
    quotes_to_follow_up = Quote.objects.filter(
        status=QuoteStatusChoices.QUOTES,  # Filter by status 'Quote'
        quote_dates__quoted__lte=seven_days_ago  # Quoted date is more than 7 days ago
    )

    # Loop through each quote and update the status
    for quote in quotes_to_follow_up:
        quote.status = QuoteStatusChoices.FOLLOWUP
        quote.save()

    return f"Updated {quotes_to_follow_up.count()} quotes to 'Follow Up'"
