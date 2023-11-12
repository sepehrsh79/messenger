from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404

from . import forms
from .models import CustomUser


def register_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.POST:
        form = forms.SaveUser(request.POST)
        if form.is_valid():
            instance = form.save()
            password = form.cleaned_data['password1']
            instance.set_password(password)
            instance.is_active = True
            instance.save()
            messages.success(request, "The Profile has been created successfully!")
            login(request, instance)
            return redirect("index")

    return render(request, 'account/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successfully!")
            return redirect("index")
        else:
            messages.warning(request, "Username or Password is not correct.")

    return render(request, 'account/login.html', )


def logout_user(request):
    logout(request)
    messages.success(request, "Logout successfully!")
    return redirect('account:login_view')


@login_required()
def edit_account(request):
    username = request.user.username
    user = CustomUser.objects.filter(username=username)
    if not user.exists():
        raise Http404('User not found!')
    user = user.first()
    if request.POST:
        edit_form = forms.UpdateProfile(request.POST, request.FILES, instance=user)
        if edit_form.is_valid():
            user = edit_form.save()
            user.save()
            messages.success(request, "Edited successfully!")
            return redirect('index')

    context = {'user': user}
    return render(request, 'account/edit_account.html', context)


def verify_view(request):
    return render(request, 'account/verify.html')

