from django.shortcuts import render,redirect
from .models import *
from .forms import PhotoForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
  
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('gallery')

    context ={
        'page':page
    }

    return render(request,'login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    
    form = UserCreationForm(request.POST)


    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            user = authenticate(request, username=user.username, password=request.POST['password1'])

            if user is not None:
                login(request,user)
                return redirect('gallery')         
    context = {
        'form': form,
        'page': page
    }
    
    return render(request, 'login_register.html' ,context)



@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user = user)
    else:
        photos = Photo.objects.filter(category__name = category, category__user = user)

    categories = Category.objects.filter(user=user)

    context = {
        'categories': categories,
        'photos' : photos
    }
    return render(request,'gallery.html',context)

@login_required(login_url='login')
def viewPhoto(request,pk):
    photos = Photo.objects.get(id=pk)
    context = {
        'photos' : photos
    }

    return render(request,'view-photo.html',context)


@login_required(login_url='login')
def addPhoto(request):
    user = request.user
    category = user.category_set.all()
    
    if request.method=='POST':
        data = request.POST
        image = request.FILES.get('image')
        
        if data['category'] != 'none':
            categories = Category.objects.get(id = data['category'])
        elif data['category_new'] != '' :
            categories,created = Category.objects.get_or_create(
                user=user, name = data['category_new'])
        else :
            categories = None

        photo = Photo.objects.create(
            category = categories,
            description = data['description'],
            image=image
        )
        
        return redirect('gallery')
    context = {        
        'category' : category
    }
    return render(request,'add-photo.html',context)

