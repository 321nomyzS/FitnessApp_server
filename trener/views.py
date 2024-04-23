from .forms import ExerciseForm
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'base.html')


def add_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = ExerciseForm()
    return render(request, 'add_exercise.html', {'form': form})


def show_exercise(request):
    return render(request, 'show_exercise.html')

def add_training(request):
    return render(request, 'add_training.html')

def show_training(request):
    return render(request, 'show_training.html')
