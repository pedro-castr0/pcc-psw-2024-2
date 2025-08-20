from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from follows.models import Follow
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

def create(request):
    if request.method == 'GET':
        return render(request, 'user/sign_up.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(
            username = username,
            email = email,
            password = password
        )

        user.save()

        return redirect('/')

def log_in(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            return redirect('home')
        
        else:
            return redirect('/user/login/')

def log_out(request):
    logout(request)
    return redirect('/user/login/')

def list(request):
    users = User.objects.all()
    return render(request, 'user/list.html', {'users':users})

def edit(request, id):
    user = User.objects.get(id = id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.password = request.POST.get('password')

        user.save()

        return redirect('/user/list/')
    
    return render(request, 'user/form.html', {'user':user})

def delete(request, id):
    user = User.objects.get(id = id)
    user.delete()

    return redirect('/user/list/')