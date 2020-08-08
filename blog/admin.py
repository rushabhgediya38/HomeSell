from django.contrib import admin
from blog.models import Post, Contact

# Register your models here.
admin.site.register(Post)


class ContactAdmib(admin.ModelAdmin):
    list_display = ('id', 'name', 'listing', 'email', 'contact_date')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'email')
    list_per_page = 25


admin.site.register(Contact, ContactAdmib)





