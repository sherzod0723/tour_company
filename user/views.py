from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .models import User
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
import random
from django.contrib.auth.hashers import make_password


def my_context_processor(request):
    context = {
        "current_site_url": get_current_site(request)
    }
    return context


def forgot_password(request, user):
    current_site = get_current_site(request)
    mail_subject = "Password Reset"
    message = render_to_string('user/reset_password.html', {
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    email = EmailMessage(
        mail_subject,
        message,
        to=[request.POST['email']],
    )
    email.send()

class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        forgot_pass = request.POST.get('forgot_password')
        if forgot_pass == "1":
            user = get_object_or_404(User, email=request.POST['email'])
            forgot_password(request, user)
            return render(request, 'user/login.html', {"link_sent": 1})
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('main_home_view')
        return render(request, 'user/login.html', {"login_error": 1})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main_home_view')


def email_send(request, user):
    current_site = get_current_site(request)
    mail_subject = f"Marokand TOUR подтверждение электронной почты"
    message = render_to_string('user/email_confirmation.html', {
        'user': user.first_name,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    email = EmailMessage(
        mail_subject,
        message,
        to=[request.POST['email']],
    )
    email.send()


class SignupView(View):
    def get(self, request):
        return render(request, 'user/signup.html')

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        check_email = User.objects.filter(email=request.POST['email'], is_active=False)
        if check_email:
            email_send(request, user=check_email.first())
            return render(request, 'user/signup.html', {"link_send": 1})
        elif form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user.is_active = False
            user.save()
            email_send(request, user)
            return render(request, 'user/signup.html', {"link_send": 1})
        context = {
            'form': form
        }
        return render(request, 'user/signup.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'user/login.html', {"email_confirmed": 1})
    else:
        return HttpResponse("This link is expired")


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        return render(request, 'user/reset_password_form.html', {"user_id": user.id})
    else:
        return HttpResponse("This link is expired")


class ResetPasswordForm(View):
    def post(self, request):
        user_id = request.POST.get('user_id')
        password = request.POST.get('password1')
        user_obj = User.objects.get(id=user_id)
        user_obj.password = make_password(password)
        user_obj.save()
        user = authenticate(request, email=user_obj.email, password=password)
        if user:
            login(request, user)
            return redirect('main_home_view')
        return render(request, 'user/login.html', {"login_error": 1})