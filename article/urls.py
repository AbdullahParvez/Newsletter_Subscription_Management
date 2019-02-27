from django.conf.urls import url
from .views import (
    post_detail_view,
    rating_list,
    rate,
    subscribe,
    unsunscribe,
    update_rate
)

urlpatterns = [
    url(r'^post/(?P<pk>\d+)/$', post_detail_view, name='post_detail'),
    url(r'^post/rate/$', rate, name='post_rate'),
    url(r'^subscribe/$', subscribe, name='subscribe'),
    url(r'^unsubscribe/$', unsunscribe, name='unsubscribe'),
    url(r'^post/rate/update/$', update_rate, name='rating_update'),
    url(r'^admin/rating/list/$', rating_list, name="post_rating_list"),
]