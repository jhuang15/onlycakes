from .models import Cake, Photo
import os
import uuid
import boto3
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class CakeCreate(LoginRequiredMixin, CreateView):
  model = Cake
  fields = ['name', 'creation_date', 'description', 'recipe', 'tags']
  success_url = '/cakes/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    super().form_valid(form)
    photo_file = self.request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, cake_id=self.object.pk)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('index')
        
class CakeUpdate(LoginRequiredMixin, UpdateView):
  model = Cake
  fields = ['name', 'description', 'recipe', 'tags']

class CakeDelete(LoginRequiredMixin, DeleteView):
  model = Cake
  success_url = '/cakes/'

@login_required
def cakes_by_tag(request, tag_slug):
  cakes = Cake.objects.filter(tags__name__in=[tag_slug])
  return render(request, 'cakes/index.html', {'cakes': cakes, 'tag': tag_slug})

def home(request):
  return render(request, 'home.html')

@login_required
def about(request):
  return render(request, 'about.html')

@login_required
def cakes_index(request):
  cakes = Cake.objects.all()
  return render(request, 'cakes/index.html', { 'cakes': cakes })

@login_required
def cakes_detail(request, cake_id):
  cake = Cake.objects.get(id=cake_id)
  return render(request, 'cakes/detail.html', { 'cake': cake})

@login_required
def cake_search(request):
  if request.method == "POST":
    searched = request.POST['searched']
    cakes = Cake.objects.filter(name__contains=searched)
    return render(request, 'main_app/cake_search.html', {'searched':searched, 'cakes':cakes})
  else:
    return render(request, 'main_app/cake_search.html', {})

@login_required
def add_photo(request, cake_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, cake_id=cake_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', cake_id=cake_id)

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