from django.shortcuts import render, Http404, HttpResponse,render_to_response
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView
from .form import PostForm, RatingForm
from .models import Post, Subscriber, Rating
from django.db.models import Avg, Sum
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.


class CreatePostView(CreateView):
    form_class = PostForm
    model = Post

    def get_success_url(self):
        return reverse('home')


class PostListView(ListView):
    model = Post

    template_name = "newsletter_subscription_management/index.html"

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        rating_form = RatingForm()
        context['rating'] = rating_form
        context['rate'] = False

        if self.request.method == 'POST':
            print(self.request)
        return context


def post_detail_view(request, pk=None, *args, **kwargs):
    # instance = Product.objects.get(pk=pk)
    # instance = Product.objects.get(pk=pk, featured=True)
    # instance = get_object_or_404(Product, pk=pk)

    instance = Post.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")

    rating_form = RatingForm()
    context = {
        'object': instance,
        'rating_form': rating_form,
    }

    if request.method == 'POST':
        # print(request.POST)
        email = request.POST.get('email')
        type = request.POST.get('type')
        print(email)
        if type == "rate":
            if not Subscriber.objects.get_by_email(email):
                subscriber = True
                context = {
                    'object': instance,
                    'rating_form': rating_form,
                    'subscriber': subscriber,
                }
                return render(request, "article/post_detail.html", context)
            else:
                rating = Rating()
                rating.post_id = Post.objects.get_by_id(request.POST.get('post'))
                rating.user_id = Subscriber.objects.get_by_email(request.POST.get('email'))
                rating.rating = request.POST.get('rating')
                rating.save()
                unsubscribe = True
                rate = request.POST.get('rating')
                email = request.POST.get('email')
                context = {
                    'object': instance,
                    'unsubscribe': unsubscribe,
                    'rate': rate,
                    'email': email,
                }
                return render(request, "article/post_detail.html", context)
                # subscriber = Subscriber.objects.get_by_email(email)
                # subscriber_id = subscriber
        elif type == "subscribe":
            subscriber = Subscriber()
            subscriber.email = request.POST.get('email')
            subscriber.subscribe = request.POST.get('subscribe')
            subscriber.save()
            context = {
                'object': instance,
                'rating_form': rating_form,
            }

        elif type == 'unsubscribe':
            subscriber = Subscriber.objects.get_by_email(request.POST.get('email'))
            subscriber.delete()
            context = {
                'object': instance,
                'rating_form': rating_form,
            }
            return render(request, "article/post_detail.html", context)

    return render(request, "article/post_detail.html", context)


def list(request):
    # list_post = Post.objects.get_post_with_rating()
    list_post = Rating.objects.values('post_id__title').annotate(avgRating=Avg('rating')).order_by('post_id')
    for l in list_post:
        print(l['post_id__title'])

    context = {
        'object_list': list_post,
        'count':0,
    }

    return render(request, 'article/list.html', context)

@staff_member_required()
def rating_list(request):
    list_post = Rating.objects.values('post_id__title').annotate(avgRating=Avg('rating')).order_by('post_id')
    context = {
        'object_list': list_post,
    }

    return render(request, 'article/post_rating_list.html', context)


def index(request):
    return render(request, 'newsletter_subscription_management/index.html', {})
