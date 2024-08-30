from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        # print(uname, email, password, confirmpassword)
        if password1 != confirmpassword:
            messages.warning(request, "Password mismatch")
            return redirect('/signup')

        # Check if the username is already taken
        if User.objects.filter(username=uname).exists():
            messages.warning(request, "Username already taken")
            return redirect('/signup')
        # Check if the email is already taken
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already taken")
            return redirect('/signup')

        myuser = User.objects.create_user(uname, email, password1) # noqa
        myuser.save()
        messages.success(request, "Signup Success please login")
        return redirect('/login')
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')
