from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Avg, Count
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import App, Review




def refresh_rating(app_id):
    stats=Review.objects.filter(app_id=app_id).aggregate(average=Avg('stars'), count=Count('stars'))
    count=stats['count'] or 0

    if stats['average'] is None:
        rating=0
    else:
        rating=Decimal(str(stats['average'])).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP )
    App.objects.filter(pk=app_id).update(average_rating=rating, count_rating=count)



@receiver(post_save, sender=Review, dispatch_uid='main.')
def review_saved(sender, instance,  **kwargs):
    refresh_rating(instance.app_id)


@receiver(post_delete, sender=Review, dispatch_uid='main.review_deleted_refresh_rating')
def review_deleted(sender, instance, **kwargs):
    refresh_rating(instance.app_id)
