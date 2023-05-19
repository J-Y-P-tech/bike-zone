from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import BaseUserManager
from contacts.models import Contact


def login(request):
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=BaseUserManager.normalize_email(email),
                                 password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        # username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
                return redirect('register')

            else:
                user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email,
                                                username=email, password=password)
                user.save()
                # Log in automatically after user registered successfully
                auth.login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('dashboard')

                # If we don't want auto log in comment the upper part and uncomment this one
                # messages.success(request, 'You are registered successfully.')
                # return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)

    data = {
        'inquiries': user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', data)
