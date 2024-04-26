from .forms import ExerciseForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import *


def home(request):
    return render(request, 'base.html')


@csrf_protect
def add_exercise(request):
    print("Baza ćwiczeń:", Exercise.objects.all())
    if request.method == 'POST':
        print(request.FILES)
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            exercise = Exercise(
                title=form.cleaned_data['title'],
                short_description=form.cleaned_data['short_description'],
                video_link=form.cleaned_data['video_link'],
                html_content=form.cleaned_data['html_content'],
                type=form.cleaned_data['type'],
                language=form.cleaned_data['language']
            )
            exercise.save()

            exercise.image = form.cleaned_data['image']
            if exercise.image:
                exercise.save()

            return redirect('home')  # Przekierowanie na inną stronę po udanym dodaniu
        else:
            return render(request, 'add_exercise.html', {'form': form})
    else:
        form = ExerciseForm()
        return render(request, 'add_exercise.html', {'form': form})


def show_exercise(request):
    return render(request, 'show_exercise.html')


def add_training(request):
    return render(request, 'add_training.html')


def show_training(request):
    return render(request, 'show_training.html')
