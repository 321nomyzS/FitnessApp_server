from .forms import ExerciseForm, MyTrainingForm, ClientForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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

            return redirect('home')  # Przekierowanie na inną stronę po udanym dodaniu
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
def add_training(request):
    exercises = Exercise.objects.all()
    if request.method == "POST":
        form = MyTrainingForm(request.POST)

        if form.is_valid():
            exercise_id_keys = [key.split('-')[2] for key in request.POST.keys() if key.startswith('exercise-id-')]
            exercise_tips_keys = [key.split('-')[2] for key in request.POST.keys() if key.startswith('exercise-tips-')]
            exercise_keys_id = list(set(exercise_id_keys) & set(exercise_tips_keys))

            if request.POST['training-type'] == 'personal':
                # Creating PersonalWorkout object
                new_training = PersonalWorkout()
                new_training.title = request.POST['title']
                new_training.workout_date = request.POST['workout_date']
                # new_training.person = request.POST['workout-person']
                new_training.visibility = request.POST['visible-radio'] == 'yes'
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
                new_training.visibility = request.POST['visible-radio'] == 'yes'

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
def add_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST, request.FILES)

        if form.is_valid():
            new_client = Client(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                status=form.cleaned_data['status'],
                active_until=form.cleaned_data['active_until']
            )

            new_client.save()

            new_client.photo = form.cleaned_data['photo']
            if new_client.photo:
                new_client.save()

            return redirect('home')
        else:
            return render(request, 'add_client.html', {'form': form})

    form = ClientForm()
    return render(request, 'add_client.html', {'form': form})


@login_required
def show_clients(request):
    clients = Client.objects.all()
    return render(request, 'show_clients.html', {"clients": clients})


@login_required
def show_client(request, id):
    client = Client.objects.get(id=id)
    return render(request, 'show_client.html', {'client': client})


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': True})

    return render(request, 'login.html')


def logout_tunnel(request):
    logout(request)
    return redirect('login')
