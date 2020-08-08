from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from blog.models import Post, Contact, State, City, Country
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from blog.choices import bedrooms_choices, price_choices
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.


def index(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/index.html', context)


class PostListView(ListView):
    # model = Post
    # template_name = 'blog/index.html'
    # context_object_name = 'posts'
    # ordering = ['-list_date']
    # paginate_by = 3
    def get(self, request, *args, **kwargs):
        posts = Post.objects.order_by('-list_date').filter(is_publice=True)
        # # that mens je first post hase te first show thase and publice  = true than show the post else not show

        country = Country.objects.all()
        state = State.objects.all()
        city = City.objects.all()

        paginator = Paginator(posts, 3)
        page = request.GET.get('page')
        page_listing = paginator.get_page(page)

        context = {
            'posts': page_listing,
            'bedrooms_choices': bedrooms_choices,
            'price_choices': price_choices,
            'country': country,
            'state': state,
            'city': city
        }

        return render(request, 'blog/index.html', context)


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-list_date')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title',
              'country',
              'state',
              'city',
              'address',
              'zipcode',
              'description',
              'price',
              'bedrooms',
              'bathrooms',
              'garage',
              'sqft',
              'lot_size',
              'photo_main',
              'photo_1',
              'photo_2',
              'photo_3',
              'photo_4',
              'photo_5',
              'photo_6',
              'is_publice',
              'list_date',
              ]

    def form_valid(self, form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['state'].queryset = State.objects.none()
            self.fields['city'].queryset = City.objects.none()

            if 'country' in self.data:
                try:
                    country_id = int(self.data.get('country'))
                    state_id = self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('name')
                    self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')

                except (ValueError, TypeError):
                    pass

            elif self.instance.pk:
                self.fields['state'].queryset = self.instance.country.state_set.order_by('name')
                self.fields['city'].queryset = self.instance.state.city_set.order_by('name')
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title',
              'country',
              'state',
              'city',
              'address',
              'zipcode',
              'description',
              'price',
              'bedrooms',
              'bathrooms',
              'garage',
              'sqft',
              'lot_size',
              'photo_main',
              'photo_1',
              'photo_2',
              'photo_3',
              'photo_4',
              'photo_5',
              'photo_6',
              'is_publice',
              ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def search(request):
    queryset_list = Post.objects.order_by('-list_date')
    country1 = Country.objects.all()
    state1 = State.objects.all()
    city1 = City.objects.all()

    # Key words
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # city

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__exact=city)

    # state

    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__exact=state)

    # country

    if 'country' in request.GET:
        country = request.GET['country']
        if country:
            queryset_list = queryset_list.filter(country__exact=country)

    # bedrooms

    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # bedrooms

    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'bedrooms_choices': bedrooms_choices,
        'price_choices': price_choices,
        'country_choices': country1,
        'state_choices': state1,
        'city_choices': city1,
        'posts': queryset_list,
        'values': request.GET

    }
    return render(request, 'blog/search.html', context)


def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'blog/city_dropdown_list_options.html', {'cities': cities})


def load_states(request):
    country_id = request.GET.get('country')
    states = State.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'blog/state_options.html', {'states': states})


def contact(request):
    if request.method == 'POST':
        listing = request.POST['listing']
        listing_id = request.POST['listing_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check user has made inquery already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this post')
                return redirect('/post/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id,
                          name=name, email=email, phone=phone,
                          message=message, user_id=user_id)
        contact.save()

        # send mail

        send_mail(
            'Property Listing Inquiry',
            'There has been an inquiry for ' + listing + ' Message: ' + message,
            'jaybhat433@gmail.com',
            [realtor_email, 'tech123@gmail.com'],
            fail_silently=False
        )

        messages.success(request, 'Your request has been submited, a realtor will get back soon')
        return redirect('/post/' + listing_id)
