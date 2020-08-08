from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse


class Country(models.Model):
    sortname = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    phonecode = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'blog_country'


class State(models.Model):
    name = models.CharField(max_length=200, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'blog_state'


class City(models.Model):
    name = models.CharField(max_length=200, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'blog_city'


class Post(models.Model):
    title = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    garage = models.IntegerField(default=0)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_publice = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        # managed = True
        db_table = 'blog_post'


class Contact(models.Model):
    listing = models.CharField(max_length=200)
    listing_id = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=datetime.now)
    user_id = models.IntegerField(blank=True)

    def __str__(self):
        return self.name
