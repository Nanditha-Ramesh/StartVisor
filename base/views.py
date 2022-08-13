from unicodedata import name
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from .forms import *


def home(request):
    
    return render(request, 'base/home.html')

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    page='login'

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or password does not exist ')    
    context = {'page':page}
    return render(request, 'base/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    context = {'form':form}
    return render(request, 'base/login.html', context)

def chat(request):
    roomMessages = Message.objects.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            body = request.POST.get('body')
        )
    return render(request, 'base/chat.html', {'roomMessages':roomMessages})