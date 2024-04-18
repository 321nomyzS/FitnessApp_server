from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'base.html')

def add_exercise(request):
    return render(request, 'add_exercise.html')

def show_exercise(request):
    return render(request, 'show_exercise.html')

def add_training(request):
    return render(request, 'add_training.html')

def show_training(request):
    return render(request, 'show_training.html')
