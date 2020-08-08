from django.urls import path
from . import views
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),  # person_changelist
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(template_name='blog/post_detail.html'), name='post-detail'),
    path('post/new/', PostCreateView.as_view(template_name='blog/post_form.html'), name='post-create'),  # person_add
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(template_name='blog/post_confirm_delete.html'),
         name='post-delete'),
    path('search', views.search, name='search'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-states/', views.load_states, name='ajax_load_states'),
    path('contact/', views.contact, name='contact'),

]
