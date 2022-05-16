from .models import Cake
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

class CakeCreate(CreateView):
  model = Cake
  fields = '__all__'
  success_url = '/cakes/'

class CakeUpdate(UpdateView):
  model = Cake
  fields = ['description', 'recipe']

class CakeDelete(DeleteView):
  model = Cake
  success_url = '/cakes/'


def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def cakes_index(request):
  cakes = Cake.objects.all()
  return render(request, 'cakes/index.html', { 'cakes': cakes })

def cakes_detail(request, cake_id):
  cake = Cake.objects.get(id=cake_id)
  return render(request, 'cakes/detail.html', { 'cake': cake})

def cake_search(request):
  if request.method == "POST":
    searched = request.POST['searched']
    cakes = Cake.objects.filter(name__contains=searched)
    return render(request, 'main_app/cake_search.html', {'searched':searched, 'cakes':cakes})
  else:
    return render(request, 'main_app/cake_search.html', {})

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - Please try again.'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)