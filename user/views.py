from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from user.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
# reset password start here
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# this is for online email verification
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import threading

# This is for validate email (install like this pip install validate-email/ and also check check_regex=True,
# check_mx=True for if user enter not valid gmail account than throw the error)
from tornado.web import authenticated
from validate_email import validate_email

from .token_generator import generate_token


# Create your views here.

class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


def register(request):
    if request.method == 'POST':
        first_name1 = request.POST['first_name']
        last_name1 = request.POST['last_name']
        username = request.POST['username']
        email1 = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        context = {
            'has_error': False
        }

        if username == '':
            messages.add_message(request, messages.ERROR, 'Username is required')
            context['has_error']: True

        if first_name1 == '':
            messages.add_message(request, messages.ERROR, 'Firstname is required')
            context['has_error']: True

        if last_name1 == '':
            messages.add_message(request, messages.ERROR, 'Lastname is required')
            context['has_error']: True

        if email1 == '':
            messages.add_message(request, messages.ERROR, 'Email is required')
            context['has_error']: True

        if password == '':
            messages.add_message(request, messages.ERROR, 'Password is required')
            context['has_error']: True

        if password2 == '':
            messages.add_message(request, messages.ERROR, 'Confirm Password is required')
            context['has_error']: True

        # username should be under 15 characters
        if len(username) > 10:
            messages.add_message(request, messages.ERROR, 'please Enter short username')
            context['has_error'] = True

        # username should be alphanumeric mens does not contain any &*()%$ etc..
        if not username.isalnum():
            messages.add_message(request, messages.ERROR, 'Username Should Be Alphanumeric')
            context['has_error'] = True

        # Username Already exists or not if yes than show this error
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Username Already Exists')
            context['has_error'] = True

        # validate email or not
        if not validate_email(email1, check_regex=True, check_mx=True):
            messages.add_message(request, messages.ERROR, 'please provide a valid Email')
            context['has_error'] = True

        # Email Already exists or not if yes than show this error
        if User.objects.filter(email=email1).exists():
            messages.add_message(request, messages.ERROR, 'Email Already Exists')
            context['has_error'] = True

        # password should match
        if password != password2:
            messages.add_message(request, messages.ERROR, 'Password Not Match')
            context['has_error'] = True

        if len(password) < 7:
            messages.add_message(request, messages.ERROR, 'password shod be Atleast 7 character or more')
            context['has_error'] = True

        # if remember1 == '':
        #     messages.add_message(request, messages.ERROR, 'Please Agree The Terms and Conditions.')
        #     context['has_error']: True

        if context['has_error']:
            return render(request, 'users/register.html', context, status=400)

        user = User.objects.create_user(username=username, email=email1, password=password)
        user.first_name = first_name1
        user.last_name = last_name1
        user.is_active = False
        user.save()
        # start here email verification online

        current_site = get_current_site(request)
        email_subject = 'Activate Your Account'
        message = render_to_string('users/activate.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': generate_token.make_token(user),

                                   }
                                   )

        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email1],

        )

        # email_message.send()
        EmailThread(email_message).start()

        messages.add_message(request, messages.SUCCESS, 'We will share you mail to activate your account')
        return render(request, 'users/register.html')

    else:
        return render(request, 'users/register.html')


def login(request):
    if request.method == 'POST':
        username1 = request.POST['username']
        password1 = request.POST['password']

        context = {
            'has_error': False
        }

        if username1 == '':
            messages.add_message(request, messages.ERROR, 'Username is required')
            context['has_error']: True

        if password1 == '':
            messages.add_message(request, messages.ERROR, 'Password is required')
            context['has_error']: True

        try:
            user = auth.authenticate(username=get(email=username1), password=password1)

        except:
            user = auth.authenticate(username=username1, password=password1)

        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, f'Welcome {user.username}')
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Please enter valid email address')
            return render(request, 'users/login.html', status=401, context=context)

    else:
        return render(request, 'users/login.html')


@login_required()
def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        messages.success(request, "logout successful")
        return redirect('/')


def ActivateAccountView(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, f'account activated successfully {user.username}')
        return render(request, 'users/login.html')
    return render(request, 'users/activate_failed.html', status=401)


def ResetPassword(request):
    if request.method == 'POST':
        email = request.POST['email']

        if not validate_email(email):
            messages.error(request, 'Please enter a valid email')
            return render(request, 'users/ForgetPassword.html')

        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_subject = 'Reset Your Password'
            message = render_to_string('users/ResetPasswordEmailForm.html',
                                       {
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                                           'token': PasswordResetTokenGenerator().make_token(user[0]),

                                       }
                                       )

            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],

            )

            # email_message.send()
            EmailThread(email_message).start()

        messages.success(request, 'We have sent you email with instruction on how to reset password')
        return render(request, 'users/ForgetPassword.html')

    return render(request, 'users/ForgetPassword.html')


def Setnewpassword(request, uidb64, token):
    if request.method == 'GET':
        context = {
            'uidb64': uidb64,
            'token': token
        }
        return render(request, 'users/set-new-password.html', context)

    if request.method == 'POST':
        context = {
            'uidb64': uidb64,
            'token': token,
            'has_error': False
        }

        password = request.POST['password']
        password1 = request.POST['password1']

        if password == '':
            messages.add_message(request, messages.ERROR, 'Password is required')
            context['has_error']: True

        if password1 == '':
            messages.add_message(request, messages.ERROR, 'Confirm Password is required')
            context['has_error']: True

        if password != password1:
            messages.add_message(request, messages.ERROR, 'Password Not Match')
            context['has_error'] = True

        if len(password) < 7:
            messages.add_message(request, messages.ERROR, 'password shod be Atleast 7 character or more')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'users/set-new-password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(request, 'password reset success, you can login with new password')
            return render(request, 'users/login.html')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Something went wrong')
            return render(request, 'users/set-new-password.html', context)

    return render(request, 'users/set-new-password.html')


@login_required()
def profile(request):
    if request.method == 'POST':
        u_Form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_Form.is_valid() and p_form.is_valid():
            u_Form.save()
            p_form.save()

            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        u_Form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_Form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
