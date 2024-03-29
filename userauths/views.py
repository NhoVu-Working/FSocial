from django.shortcuts import render, redirect, reverse
from userauths.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from userauths.models import Profile, User
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm


def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey {request.user.username}, you are already logged in")
        return redirect('core:feed')

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get('full_name')
        phone = form.cleaned_data.get('phone')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        user = authenticate(email=email, password=password)
        login(request, user)

        messages.success(request, f"Hi {request.user.username}, your account have been created successfully.")

        profile = Profile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()

        return redirect('core:feed')

    context = {'form': form}
    return render(request, 'userauths/login_register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already login!")
        return redirect('core:feed')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            login(request, user)
            if user is not None:
                messages.success(request, f"Hi {user.full_name}.your account was created successfully")
                return redirect('core:feed')
            else:
                messages.warning(request, "Invalid email or password")
                return redirect('userauths:register')
        except User.DoesNotExist:
            messages.warning(request, "Invalid email or password")
            return redirect('userauths:sign-up')
    return HttpResponseRedirect("/")


def logout_view(request):
    logout(request)
    return redirect('userauths:sign-up')
