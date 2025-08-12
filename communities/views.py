from django.shortcuts import render, redirect
from .models import Community
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

def create(request):
    if request.method == 'GET':
        return render(request, 'community/form.html')
    
    elif request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        tag = request.POST.get('tag')
        created = request.POST.get('created')
        creator_id = request.POST.get('creator')
        creator = User.objects.get(id = creator_id) 


        community = Community(
            name = name,
            description = description,
            tag = tag,
            created = created,
            creator = creator
        )

        community.save()

    return redirect('/community/list/')

def list(request):
    communities = Community.objects.all()
    return render(request, 'community/list.html', {'communities':communities})

def edit(request, id):
    community = Community.objects.get(id = id)

    if request.method == 'POST':
        community.name = request.POST.get('name')
        community.description = request.POST.get('description')
        community.tag = request.POST.get('tag')

        community.save()

        return redirect('/community/list/')
    
    return render(request, 'community/form.html', {'community':community})


def delete(request, id):
    community = Community.objects.get(id = id)
    community.delete()

    return redirect('/community/list/')

def page(request, id):
    community = Community.objects.get(id = id)
    return render(request, 'community/page.html', {'community':community})


