from .forms import ExerciseForm, MyTrainingForm, ClientForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
import os
import shutil
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .forms import ExerciseForm, MyTrainingForm, PlantForm
# from .models import Plant, WaterNeed, LightRequirement, CareLevel, Exercise, GeneralWorkout, PersonalWorkout, WorkoutExercise


@login_required
def home(request):
    return render(request, 'base.html')

from django.db import models



def plant_list(request):
    plants = Plant.objects.all()
    return render(request, 'plant_list.html', {'plants': plants})


def add_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PlantForm()

    return render(request, 'add_plant.html', {'form': form})

def delete_plant(request, id):
    plant = get_object_or_404(Plant, id=id)
    plant.delete()
    return redirect(reverse('plant_list'))

def edit_plant(request, id):
    plant = get_object_or_404(Plant, id=id)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('show_plants')  # Zmień na odpowiednią nazwę widoku listy roślin
    else:
        form = PlantForm(instance=plant)
    return render(request, 'edit_plant.html', {'form': form, 'plant': plant})

@login_required
def assign_plant_to_user(request):
    user = request.user
    person = Person.objects.get(user=user)

    if request.method == 'POST':
        plant_id = request.POST.get('plant_id')
        plant = Plant.objects.get(id=plant_id)
        person.plants.add(plant)  # Dodanie rośliny do konta użytkownika
        return redirect('profile')

    plants = Plant.objects.all()
    return render(request, 'assign_plant.html', {'plants': plants})

def show_plants(request):
    plants = Plant.objects.all()  # Pobieranie wszystkich roślin z bazy danych
    return render(request, 'show_plants.html', {'plants': plants})
def show_plant(request, id):
    plant = get_object_or_404(Plant, id=id)
    return render(request, 'show_plant.html', {'plant': plant})

@login_required
def show_user_plants(request):
    user = request.user
    person = Person.objects.get(user=user)
    plants = person.plants.all()  # Rośliny przypisane do użytkownika
    return render(request, 'user_plants.html', {'plants': plants})

@login_required
def show_exercises(request):
    exercises = Exercise.objects.all()
    return render(request, 'show_plants.html', {"exercises": exercises})


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
            print("Form is not valid")
            print(form.errors)
    else:
        form = ExerciseForm(instance=exercise)

    return render(request, 'edit_exercise.html', {'form': form, 'exercise': exercise})

@login_required
def delete_exercise(request, id):
    if request.method == 'POST':
        exercise = get_object_or_404(Exercise, id=id)
        exercise_dir = os.path.join(settings.MEDIA_ROOT, f'exercise/{exercise.id}')

        exercise.delete()

        # Usuń katalog ćwiczenia po usunięciu ćwiczenia
        if os.path.exists(exercise_dir):
            shutil.rmtree(exercise_dir)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)


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

            print("exercise_id_keys:", exercise_id_keys)
            print("exercise_tips_keys:", exercise_tips_keys)
            print("exercise_keys_id:", exercise_keys_id)

            if request.POST['training-type'] == 'personal':
                new_training = PersonalWorkout()
                new_training.title = request.POST['title']
                new_training.workout_date = request.POST['workout_date']
                new_training.visibility = request.POST['visible-radio'] == 'yes'
                new_training.client = Person.objects.get(id=request.POST['workout-person'])
                new_training.save()

                for key_id in exercise_keys_id:
                    print(f"Przetwarzanie ćwiczenia {key_id}")
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
                    print(f"Przetwarzanie ćwiczenia {key_id}")
                    workout_exercise = WorkoutExercise()
                    workout_exercise.general_workout = new_training
                    workout_exercise.exercise = Exercise.objects.get(id=request.POST[f'exercise-id-{key_id}'])
                    workout_exercise.comment = request.POST[f'exercise-tips-{key_id}']
                    workout_exercise.save()

            return redirect('show_training')

        else:
            print("Formularz jest niepoprawny:", form.errors)
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


#@login_required
def show_personal_training(request, id):
    if request.user.is_authenticated:
        personal_training = PersonalWorkout.objects.get(id=id)
        workout_exercises = WorkoutExercise.objects.filter(personal_workout_id=id)
        return render(request, 'show_training.html', {'training': personal_training, 'workout_exercises': workout_exercises})
    else:
        # Obsłuż przypadek, gdy użytkownik jest anonimowy
        return redirect('login')  # lub inna odpowiednia akcja

@login_required
@csrf_protect
def edit_general_training(request, id):
    training = get_object_or_404(GeneralWorkout, id=id)
    workout_exercises = WorkoutExercise.objects.filter(general_workout_id=id)
    exercises = Exercise.objects.all()

    if request.method == 'POST':
        training.title = request.POST['title']
        training.visibility = request.POST['visible-radio'] == 'yes'

        # Aktualizacja istniejących ćwiczeń
        existing_exercise_ids = []
        for workout_exercise in workout_exercises:
            if f'exercise-id-{workout_exercise.id}' in request.POST:
                workout_exercise.comment = request.POST.get(f'exercise-tips-{workout_exercise.id}', workout_exercise.comment)
                workout_exercise.exercise_id = request.POST.get(f'exercise-id-{workout_exercise.id}', workout_exercise.exercise.id)
                workout_exercise.save()
                existing_exercise_ids.append(str(workout_exercise.id))

        # Usuwanie istniejących ćwiczeń, które zostały usunięte z formularza
        for workout_exercise in workout_exercises:
            if str(workout_exercise.id) not in existing_exercise_ids:
                workout_exercise.delete()

        # Obsługa nowych ćwiczeń
        new_exercise_ids = [key.split('-')[2] for key in request.POST.keys() if key.startswith('exercise-id-') and key.split('-')[2].isdigit() and int(key.split('-')[2]) > len(workout_exercises)]
        for new_id in new_exercise_ids:
            exercise_id = request.POST.get(f'exercise-id-{new_id}')
            comment = request.POST.get(f'exercise-tips-{new_id}')
            if exercise_id and comment:
                WorkoutExercise.objects.create(general_workout=training, exercise_id=exercise_id, comment=comment)

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

        # Aktualizacja istniejących ćwiczeń
        existing_exercise_ids = []
        for workout_exercise in workout_exercises:
            if f'exercise-id-{workout_exercise.id}' in request.POST:
                workout_exercise.comment = request.POST.get(f'exercise-tips-{workout_exercise.id}', workout_exercise.comment)
                workout_exercise.exercise_id = request.POST.get(f'exercise-id-{workout_exercise.id}', workout_exercise.exercise.id)
                workout_exercise.save()
                existing_exercise_ids.append(str(workout_exercise.id))

        # Usuwanie istniejących ćwiczeń, które zostały usunięte z formularza
        for workout_exercise in workout_exercises:
            if str(workout_exercise.id) not in existing_exercise_ids:
                workout_exercise.delete()

        # Obsługa nowych ćwiczeń
        new_exercise_ids = [key.split('-')[2] for key in request.POST.keys() if key.startswith('exercise-id-') and key.split('-')[2].isdigit() and int(key.split('-')[2]) > len(workout_exercises)]
        for new_id in new_exercise_ids:
            exercise_id = request.POST.get(f'exercise-id-{new_id}')
            comment = request.POST.get(f'exercise-tips-{new_id}')
            if exercise_id and comment:
                WorkoutExercise.objects.create(personal_workout=training, exercise_id=exercise_id, comment=comment)

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
    print(users)
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
