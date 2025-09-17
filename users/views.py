from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# As importações já estavam aqui, vamos usá-las.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404 # Boa prática para obter objetos

# A view de criação de usuário (cadastro) deve ser pública.
# Nenhuma alteração aqui.
def create(request):
    if request.method == 'GET':
        return render(request, 'user/form.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # create_user já lida com o hash da senha corretamente.
        user = User.objects.create_user(
            username = username,
            email = email,
            password = password
        )

        return redirect('/')

# A view de login também deve ser pública.
# Nenhuma alteração aqui.
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
            # É uma boa prática mostrar uma mensagem de erro.
            # Por simplicidade, mantemos o redirecionamento.
            return redirect('/user/login/')

<<<<<<< HEAD
=======
# É uma boa prática exigir que o usuário esteja logado para fazer logout.
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
@login_required
def log_out(request):
    logout(request)
    return redirect('/user/login/')

<<<<<<< HEAD
@login_required
@permission_required('users.view_user')
=======
# A lista de todos os usuários é uma view administrativa.
@login_required
@permission_required('auth.view_user', raise_exception=True)
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
def list(request):
    users = User.objects.all()
    return render(request, 'user/list.html', {'users':users})

<<<<<<< HEAD
@login_required
@permission_required('users.change_user')
=======
# Editar um usuário é uma ação administrativa crítica.
@login_required
@permission_required('auth.change_user', raise_exception=True)
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
def edit(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        password = request.POST.get('password')

        # CORREÇÃO DE SEGURANÇA CRÍTICA:
        # NUNCA salve a senha diretamente. Use set_password() para criptografá-la.
        # Verificamos se uma nova senha foi fornecida antes de alterá-la.
        if password:
            user.set_password(password)

        user.save()

        return redirect('/user/list/')
    
    return render(request, 'user/form.html', {'user':user})

<<<<<<< HEAD
@login_required
@permission_required('users.delete_user')
=======
# Deletar um usuário é a ação mais destrutiva.
@login_required
@permission_required('auth.delete_user', raise_exception=True)
>>>>>>> d3fda6153cad5849a46df16316911fee48a79ab9
def delete(request, id):
    user = get_object_or_404(User, id=id)
    # Adicionar uma verificação para não permitir que o admin se delete
    if request.user.id != user.id:
        user.delete()

    return redirect('/user/list/')