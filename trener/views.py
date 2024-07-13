from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
import shutil
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .forms import ExerciseForm, MyTrainingForm, ClientForm
from .models import Exercise, GeneralWorkout, PersonalWorkout, WorkoutExercise


@login_required
def home(request):
    return render(request, 'base.html')


@login_required
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

            return redirect('show_exercise')
        else:
            return render(request, 'add_exercise.html', {'form': form})
    else:
        form = ExerciseForm()
        return render(request, 'add_exercise.html', {'form': form})


@login_required
def show_exercises(request):
    exercises = Exercise.objects.all()
    return render(request, 'show_exercises.html', {"exercises": exercises})


@login_required
def show_exercise(request, id):
    exercise = Exercise.objects.get(id=id)
    return render(request, 'show_exercise.html', {"exercise": exercise})


@login_required
def edit_exercise(request, id):
    exercise = get_object_or_404(Exercise, id=id)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES, instance=exercise)

        if form.is_valid():
            # Usuń stare zdjęcie, jeśli przesyłane jest nowe
            if 'image' in request.FILES:
                if exercise.image:
                    old_image_path = exercise.image.path
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

            updated_exercise = form.save(commit=False)
            updated_exercise.save()

            return redirect('/exercise')  # Przekierowanie do listy ćwiczeń
    else:
        form = ExerciseForm(instance=exercise)

    return render(request, 'edit_exercise.html', {'form': form, 'exercise': exercise})


@login_required
def delete_exercise(request, id):
    exercise = get_object_or_404(Exercise, id=id)
    exercise_dir = os.path.join(settings.MEDIA_ROOT, f'exercise/{exercise.id}')

    exercise.delete()

    if os.path.exists(exercise_dir):
        shutil.rmtree(exercise_dir)

    return redirect('show_exercise')


@login_required
@csrf_protect
def add_training(request):
    exercises = Exercise.objects.all()
    clients = Person.objects.all()

    if request.method == "POST":
        form = MyTrainingForm(request.POST)

        if form.is_valid():
            exercise_id_keys = [key.split('-')[2] for key in request.POST.keys() if key.startswith('exercise-id-')]
            exercise_tips_keys = [key.split('-')[2] for key in request.POST.keys() if key.startswith('exercise-tips-')]
            exercise_keys_id = list(set(exercise_id_keys) & set(exercise_tips_keys))

            if request.POST['training-type'] == 'personal':
                new_training = PersonalWorkout()
                new_training.title = request.POST['title']
                new_training.workout_date = request.POST['workout_date']
                new_training.visibility = request.POST['visible-radio'] == 'yes'
                new_training.client = Person.objects.get(id=request.POST['workout-person'])
                new_training.save()

                for key_id in exercise_keys_id:
                    workout_exercise = WorkoutExercise()
                    workout_exercise.personal_workout = new_training
                    workout_exercise.exercise = Exercise.objects.get(id=request.POST[f'exercise-id-{key_id}'])
                    workout_exercise.comment = request.POST[f'exercise-tips-{key_id}']
                    workout_exercise.save()

            elif request.POST['training-type'] == 'general':
                new_training = GeneralWorkout()
                new_training.title = request.POST['title']
                new_training.visibility = request.POST['visible-radio'] == 'yes'
                new_training.save()

                for key_id in exercise_keys_id:
                    workout_exercise = WorkoutExercise()
                    workout_exercise.general_workout = new_training
                    workout_exercise.exercise = Exercise.objects.get(id=request.POST[f'exercise-id-{key_id}'])
                    workout_exercise.comment = request.POST[f'exercise-tips-{key_id}']
                    workout_exercise.save()

            return redirect('show_training')

        else:
            return render(request, 'add_training.html', {'exercises': exercises, 'form': form, 'clients': clients})

    return render(request, 'add_training.html', {'exercises': exercises, 'clients': clients})


@login_required
def show_training(request):
    general_workout = GeneralWorkout.objects.all()
    personal_workout = PersonalWorkout.objects.all()

    return render(request, 'show_trainings.html', {
        'general_workout': general_workout,
        'personal_workout': personal_workout
    })


@login_required
def show_general_training(request, id):
    general_training = GeneralWorkout.objects.get(id=id)
    workout_exercises = WorkoutExercise.objects.filter(general_workout_id=id)

    return render(request, 'show_training.html', {'training': general_training, 'workout_exercises': workout_exercises})


@login_required
def show_personal_training(request, id):
    personal_training = PersonalWorkout.objects.get(id=id)
    workout_exercises = WorkoutExercise.objects.filter(personal_workout_id=id)
    return render(request, 'show_training.html', {'training': personal_training, 'workout_exercises': workout_exercises})


@login_required
@csrf_protect
def edit_general_training(request, id):
    training = get_object_or_404(GeneralWorkout, id=id)
    workout_exercises = WorkoutExercise.objects.filter(general_workout_id=id)
    exercises = Exercise.objects.all()

    if request.method == 'POST':
        training.title = request.POST['title']
        training.visibility = request.POST['visible-radio'] == 'yes'

        # Processing workout exercises
        # Deleting old workout exercises
        workout_exercises = WorkoutExercise.objects.filter(general_workout=training)
        for workout_exercise in workout_exercises:
            workout_exercise.delete()

        # Adding new workout exercises
        exercise_id_keys = [key.split('-')[2] for key in request.POST.keys() if key.startswith('exercise-id-')]
        exercise_tips_keys = [key.split('-')[2] for key in request.POST.keys() if key.startswith('exercise-tips-')]
        exercise_keys_id = list(set(exercise_id_keys) & set(exercise_tips_keys))

        for key_id in exercise_keys_id:
            workout_exercise = WorkoutExercise()
            workout_exercise.general_workout = training
            workout_exercise.exercise = Exercise.objects.get(id=request.POST[f'exercise-id-{key_id}'])
            workout_exercise.comment = request.POST[f'exercise-tips-{key_id}']
            workout_exercise.save()

        training.save()
        return redirect('show_training')

    return render(request, 'edit_training.html',
                  {'training': training, 'workout_exercises': workout_exercises, 'exercises': exercises})


@login_required
@csrf_protect
def edit_personal_training(request, id):
    training = get_object_or_404(PersonalWorkout, id=id)
    workout_exercises = WorkoutExercise.objects.filter(personal_workout_id=id)
    exercises = Exercise.objects.all()
    clients = Person.objects.all()

    if request.method == 'POST':
        training.title = request.POST['title']
        training.visibility = request.POST['visible-radio'] == 'yes'
        training.workout_date = request.POST['workout_date']
        training.client_id = request.POST['workout-person']

        # Processing workout exercises
        # Deleting old workout exercises
        workout_exercises = WorkoutExercise.objects.filter(personal_workout=training)
        for workout_exercise in workout_exercises:
            workout_exercise.delete()

        # Adding new workout exercises
        exercise_id_keys = [key.split('-')[2] for key in request.POST.keys() if key.startswith('exercise-id-')]
        exercise_tips_keys = [key.split('-')[2] for key in request.POST.keys() if key.startswith('exercise-tips-')]
        exercise_keys_id = list(set(exercise_id_keys) & set(exercise_tips_keys))

        for key_id in exercise_keys_id:
            workout_exercise = WorkoutExercise()
            workout_exercise.personal_workout = training
            workout_exercise.exercise = Exercise.objects.get(id=request.POST[f'exercise-id-{key_id}'])
            workout_exercise.comment = request.POST[f'exercise-tips-{key_id}']
            workout_exercise.save()

        training.save()
        return redirect('show_training')

    return render(request, 'edit_training.html',
                  {'training': training, 'workout_exercises': workout_exercises, 'exercises': exercises, 'clients': clients})


@login_required
def add_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST, request.FILES)

        if form.is_valid():
            new_client = Person(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                status=form.cleaned_data['status'],
                active_until=form.cleaned_data['active_until']
            )

            new_client.set_password(form.cleaned_data['password'])
            new_client.save()

            new_client.photo = form.cleaned_data['photo']
            if new_client.photo:
                new_client.save()

            return redirect('show_clients')
        else:
            return render(request, 'add_client.html', {'form': form})

    form = ClientForm()
    return render(request, 'add_client.html', {'form': form})


@login_required
def show_clients(request):
    clients = Person.objects.all()
    return render(request, 'show_clients.html', {"clients": clients})


@login_required
def show_client(request, id):
    client = Person.objects.get(id=id)
    return render(request, 'show_client.html', {'client': client})


def login_page(request):
    users=Person.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # if user.is_superuser == 0:
        #     return render(request, 'login.html', {'error': True})
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': True})

    return render(request, 'login.html')


def logout_tunnel(request):
    logout(request)
    return redirect('login')
