from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    form = AuthenticationForm(request, request.POST)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, f'{form.get_user()} залогінівся')
            return redirect('introduction:welcome')
        else:
            for field, errors in form.errors.items():
                messages.error(request, f'Ви ввели неправильно юзера або пароль. {field} - {errors}')
    return render(request, 'registration/login.html', {'form': form})

def signup_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'{user} зареєструвався')
            return redirect('introduction:welcome')
        else:
            for field, errors in form.errors.items():
                messages.error(request, f'Ви ввели неправильно юзера, або пароль, або стверджувальний пароль. {field} - {errors}')
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Ви вийшли зі свого акаунту')
    return redirect('introduction:welcome')
