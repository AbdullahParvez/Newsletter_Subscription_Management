from django.shortcuts import render, Http404, HttpResponse,render_to_response, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView
from .form import PostForm, RatingForm, SubscriberForm
from .models import Post, Subscriber, Rating
from django.db.models import Avg, Sum
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


#@user_passes_test(lambda u: u.is_superuser)
class CreatePostView(CreateView):
    form_class = PostForm
    model = Post

    def get_success_url(self):
        return reverse('home')


class PostListView(ListView):
    model = Rating

    template_name = "newsletter_subscription_management/index.html"

    @cache_page(CACHE_TTL)
    def get_queryset(self):
        return Rating.objects.values('post_id__id','post_id__title','post_id__published_date').annotate(avgRating=Avg('rating')).order_by('post_id')


# @cache_page(CACHE_TTL)
def post_list_view(request):
    instance = Rating.objects.values('post_id__id','post_id__title','post_id__published_date').annotate(avgRating=Avg('rating')).order_by('post_id')
    context = {
        'rating_list':instance
    }
    return render(request, 'newsletter_subscription_management/index.html', context)


def post_detail_view(request, pk=None):
    instance = Post.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")

    rating_form = RatingForm()
    context = {
        'object': instance,
        'rating_form': rating_form,
    }

    return render(request, "article/post_detail.html", context)


def rate(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        post_id = request.POST.get('post')
        user_id = Subscriber.objects.get_by_email(request.POST.get('email'))
        # print(user_id)
        qs = Rating.objects.filter(post_id__id__exact=post_id, user_id__email__exact=user_id )
        #print(qs)

        if not Subscriber.objects.get_by_email(email):
            return redirect("article:subscribe")

        elif qs.exists():
            instance = Post.objects.get_by_id(post_id)
            rate = request.POST.get('rating')
            email = request.POST.get('email')
            context = {
            'object': instance,
            'rate': rate,
            'email': email,
            }
            return render(request, "article/rating_update.html", context)

        else:
            rating = Rating()
            rating.post_id = post_id
            rating.user_id = user_id
            rating.rating = request.POST.get('rating')
            rating.save()
            rate = request.POST.get('rating')
            email = request.POST.get('email')
            context = {
                'object': post_id,
                'rate': rate,
                'email': email,
            }
            return render(request, "article/unsubscribe.html", context)


def update_rate(request):
    if request.POST:
        post_id = request.POST.get('post_id')
        user_id = Subscriber.objects.get_by_email(request.POST.get('email'))
        object = Rating.objects.get(post_id=post_id, user_id=user_id)
        object.rating = request.POST.get('rating')
        object.save()
        return redirect('home')



def unsunscribe(request):
    if request.method == 'POST':
        subscriber = Subscriber.objects.get_by_email(request.POST.get('email'))
        subscriber.delete()
    return render(request, "article/unsubscribe_success.html")


def subscribe(request):
    form = SubscriberForm()
    context = {
        'form': form
        }
    if request.method == 'POST':
        subscriber = Subscriber()
        subscriber.email = request.POST.get('email')
        subscriber.subscribe = True
        subscriber.save()
        return redirect("home")
    return render(request, "article/subscribe.html", context)


@staff_member_required()
##@cache_page(CACHE_TTL)
def rating_list(request):
    list_post = Rating.objects.values('post_id__title').annotate(avgRating=Avg('rating')).order_by('post_id')
    context = {
        'object_list': list_post,
    }

    return render(request, 'article/post_rating_list.html', context)



#
# class PostDetailView(DetailView):
#     model = Post
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(PostDetailView, self).get_context_data(*args, **kwargs)
#         rating_form = RatingForm()
#         context['rating'] = rating_form
#         context['rate'] = False
#
#         if self.request.method == 'POST':
#             print(self.request)
#         return context
#
# def index(request):
#     print("User is superuser; " + str(request.user.is_superuser))
#     return render(request, 'newsletter_subscription_management/index.html', {})

