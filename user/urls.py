from django.urls import path, include
from . import views
# from .views import PostCreateView

urlpatterns = [
    path('register', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('profile/', views.profile, name='profile'),
    path('ResetPassword', views.ResetPassword, name='ResetPassword'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView, name='activate'),
    path('set-new-password/<uidb64>/<token>', views.Setnewpassword, name='set-new-password'),
]
