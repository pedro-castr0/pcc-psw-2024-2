from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404

def create(request):
    if request.method == 'GET':
        return render(request, 'user/form.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(
            username = username,
            email = email,
            password = password
        )

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

@login_required
def log_out(request):
    logout(request)
    return redirect('/user/login/')

@login_required
@permission_required('users.view_user', raise_exception=True)

def list(request):
    users = User.objects.all()
    return render(request, 'user/list.html', {'users':users})

@login_required
@permission_required('users.change_user')
def edit(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        password = request.POST.get('password')

        if password:
            user.set_password(password)

        user.save()

        return redirect('/user/list/')
    
    return render(request, 'user/form.html', {'user':user})

@login_required
@permission_required('users.delete_user')
def delete(request, id):
    user = get_object_or_404(User, id=id)
    if request.user.id != user.id:
        user.delete()

    return redirect('/user/list/')