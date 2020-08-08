from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title',
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
                  )

        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control'}),
        #     'state': forms.Select(attrs={'class': 'form-control'}),
        #     'city': forms.Select(attrs={'class': 'form-control'}),
        #     'address': forms.TextInput(attrs={'class': 'form-control'}),
        #     'zipcode': forms.IntegerField(attrs={'class': 'form-control'}),
        #     'description': forms.Textarea(attrs={'class': 'form-control'}),
        #     'price': forms.IntegerField(attrs={'class': 'form-control'}),
        #     'bedrooms': forms.IntegerField(attrs={'class': 'form-control'}),
        #     'bathrooms': forms.IntegerField(attrs={'class': 'form-control'}),
        #     'garage': forms.IntegerField(attrs={'class': 'form-control'}),
        #     'sqft': forms.IntegerField(attrs={'class': 'form-control'}),
        #     'lot_size': forms.IntegerField(attrs={'class': 'form-control'}),
        #     'photo_main': forms.ImageField(attrs={'class': 'form-control-file'}),
        #     'photo_1': forms.ImageField(attrs={'class': 'form-control-file'}),
        #     'photo_2': forms.ImageField(attrs={'class': 'form-control-file'}),
        #     'photo_4': forms.ImageField(attrs={'class': 'form-control-file'}),
        #     'photo_5': forms.ImageField(attrs={'class': 'form-control-file'}),
        #     'photo_6': forms.ImageField(attrs={'class': 'form-control-file'}),
        #     'is_publice': forms.BooleanField(),
        #     'list_date': forms.DateTimeField(attrs={'class': 'form-control'}),
        # }
