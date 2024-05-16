from .forms import ExerciseForm, MyTrainingForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import *


def home(request):
    return render(request, 'base.html')


@csrf_protect
def add_exercise(request):
    if request.method == 'POST':
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


def show_exercises(request):
    exercises = Exercise.objects.all()
    return render(request, 'show_exercises.html', {"exercises": exercises})


def show_exercise(request, id):
    exercise = Exercise.objects.get(id=id)
    return render(request, 'show_exercise.html', {"exercise": exercise})


def add_training(request):
    exercises = Exercise.objects.all()
    if request.method == "POST":
        form = MyTrainingForm(request.POST)

        if form.is_valid():
            exercise_id_keys = [key.split('-')[2] for key in request.POST.keys() if key.startswith('exercise-id-')]
            exercise_tips_keys = [key for key in request.POST.keys() if key.startswith('exercise-tips-')]
            exercise_keys_id = list(set(exercise_id_keys) & set(exercise_tips_keys))

            if request.POST['training-type'] == 'personal':
                # Creating PersonalWorkout object
                new_training = PersonalWorkout()
                new_training.title = request.POST['title']
                new_training.workout_date = request.POST['workout_date']
                # new_training.person = request.POST['workout-person']
                new_training.save()

                # Creating WorkoutExercise objects
                for key_id in exercise_keys_id:
                    workout_exercise = WorkoutExercise()
                    workout_exercise.personal_workout = new_training
                    workout_exercise.exercise = Exercise.objects.get(id=request.POST[f'exercise-id-{key_id}'])
                    workout_exercise.comment = request.POST[f'exercise-tips-{key_id}']

                    workout_exercise.save()

            elif request.POST['training-type'] == 'general':
                # Creating GeneralWorkout object
                new_training = GeneralWorkout()
                new_training.title = request.POST['title']
                new_training.save()

                # Creating WorkoutExercise objects
                for key_id in exercise_keys_id:
                    workout_exercise = WorkoutExercise()
                    workout_exercise.general_workout = new_training
                    workout_exercise.exercise = Exercise.objects.get(id=request.POST[f'exercise-id-{key_id}'])
                    workout_exercise.comment = request.POST[f'exercise-tips-{key_id}']

                    workout_exercise.save()

            return redirect('show_training')

        else:
            return render(request, 'add_training.html', {'exercises': exercises, 'form': form})

    return render(request, 'add_training.html', {'exercises': exercises})


def show_training(request):
    general_workout = GeneralWorkout.objects.all()
    personal_workout = PersonalWorkout.objects.all()

    return render(request, 'show_trainings.html', {
        'general_workout': general_workout,
        'personal_workout': personal_workout
    })
