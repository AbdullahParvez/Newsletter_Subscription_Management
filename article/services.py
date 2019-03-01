from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .models import Post, Subscriber, Rating
from django.db.models import Avg

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def get_avg_rating_with_cache():
    if 'ratings' in cache:
        ratings = cache.get('ratings')
    else:
        ratings = list(Rating.objects.values('post_id__id','post_id__title','post_id__published_date').annotate(avgRating=Avg('rating')).order_by('post_id'))
        cache.set('ratings', ratings, timeout=CACHE_TTL)
    return ratings