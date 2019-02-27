from django.db import models
from django.utils import timezone
from django.db.models import Avg


class PostManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get_post_with_rating(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date').annotate(average_rating=Avg('rating'))


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)

    objects = PostManager()

    def __str__(self):
        return self.title


class SubscriberManager(models.Manager):
    def get_by_email(self, email):
        qs = self.get_queryset().filter(email=email)
        if qs.count() == 1:
            return qs.first()
        return None



class Subscriber(models.Model):
    email = models.EmailField(max_length=120,unique=True)
    subscribe = models.BooleanField(default=False)

    objects = SubscriberManager()

    def __str__(self):
        return self.email


class RatingManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None


class Rating(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    objects = RatingManager()

    class Meta:
        unique_together = ('post_id', 'user_id',)

    def __str__(self):
        return self.post_id.title +" : "+self.user_id.email+ " : "+str(self.rating)

