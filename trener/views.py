from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
import shutil
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from .forms import ExerciseForm, MyTrainingForm, ClientForm
from .models import Exercise, GeneralWorkout, PersonalWorkout, WorkoutExercise


@login_required
def home(request):
    return render(request, 'base.html')


@login_required
@csrf_protect
def add_exercise(request):
    muscle_tags = MuscleTag.objects.all()
    exercise_type_tags = ExerciseTypeTag.objects.all()

    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            exercise = Exercise(
                title=form.cleaned_data['title'],
                short_description=form.cleaned_data['short_description'],
                video_link=form.cleaned_data['video_link'],
                html_content=form.cleaned_data['html_content'],
                language=form.cleaned_data['language']
            )
            exercise.save()

            exercise.image = form.cleaned_data['image']
            if exercise.image:
                exercise.save()

            # Dodawanie tagów
            exercise_type_tag_pattern = "exercise-type-tag"
            muscle_tag_pattern = "muscle-tag"
            for key in request.POST:
                if key[:len(exercise_type_tag_pattern)] == exercise_type_tag_pattern:
                    if request.POST[key] == 'on':
                        tag_id = key.split('-')[-1]
                        tag = ExerciseTypeTag.objects.get(id=tag_id)
                        exercise.exercise_type_tags.add(tag)
                if key[:len(muscle_tag_pattern)] == muscle_tag_pattern:
                    if request.POST[key] == 'on':
                        tag_id = key.split('-')[-1]
                        tag = MuscleTag.objects.get(id=tag_id)
                        exercise.muscle_tags.add(tag)
            return redirect('show_exercise')
        else:
            return render(request, 'add_exercise.html', {'form': form})
    else:
        form = ExerciseForm()
        return render(request, 'add_exercise.html', {'form': form,
                                                     'muscle_tags': muscle_tags,
                                                     'exercise_type_tags': exercise_type_tags})


@login_required
def show_exercises(request):
    exercises = Exercise.objects.all()
    return render(request, 'show_exercises.html', {"exercises": exercises})


@login_required
def show_exercise(request, id):
    exercise = Exercise.objects.get(id=id)
    muscle_tags = MuscleTag.objects.all()
    exercise_type_tags = ExerciseTypeTag.objects.all()
    return render(request, 'show_exercise.html', {"exercise": exercise, 'muscle_tags': muscle_tags,
                                                  'exercise_type_tags': exercise_type_tags})


@login_required
def edit_exercise(request, id):
    exercise = get_object_or_404(Exercise, id=id)
    muscle_tags = MuscleTag.objects.all()
    exercise_type_tags = ExerciseTypeTag.objects.all()

    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES, instance=exercise)

        if form.is_valid():
            updated_exercise = form.save(commit=False)
            updated_exercise.save()

            # Usuwanie poprzednich tagów
            all_exercise_type_tags = ExerciseTypeTag.objects.all()
            for tag in all_exercise_type_tags:
                updated_exercise.exercise_type_tags.remove(tag)

            all_muscle_tags = MuscleTag.objects.all()
            for tag in all_muscle_tags:
                updated_exercise.muscle_tags.remove(tag)

            # Dodawanie tagów
            exercise_type_tag_pattern = "exercise-type-tag"
            muscle_tag_pattern = "muscle-tag"
            for key in request.POST:
                if key[:len(exercise_type_tag_pattern)] == exercise_type_tag_pattern:
                    if request.POST[key] == 'on':
                        tag_id = key.split('-')[-1]
                        tag = ExerciseTypeTag.objects.get(id=tag_id)
                        updated_exercise.exercise_type_tags.add(tag)
                if key[:len(muscle_tag_pattern)] == muscle_tag_pattern:
                    if request.POST[key] == 'on':
                        tag_id = key.split('-')[-1]
                        tag = MuscleTag.objects.get(id=tag_id)
                        updated_exercise.muscle_tags.add(tag)
            updated_exercise.save()

            return redirect('show_exercise')
    else:
        form = ExerciseForm(instance=exercise)

    return render(request, 'edit_exercise.html', {'form': form, 'exercise': exercise, 'muscle_tags': muscle_tags,
                                                  'exercise_type_tags': exercise_type_tags})


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

    if request.method == 'POST':
        form = MyTrainingForm(request.POST)

        if form.is_valid():
            # Creating new training
            if request.POST['training-type'] == 'personal':
                new_training = PersonalWorkout()
                new_training.title = request.POST['title']
                new_training.workout_date = request.POST['workout_date']
                new_training.visibility = request.POST['visible-radio'] == 'yes'
                new_training.client = Person.objects.get(id=request.POST['workout-person'])
                new_training.save()

                # Add exercises
                row_count = int(request.POST['rowCount'])
                for i in range(1, row_count + 1):
                    exercise_id = request.POST[f'exercise-{str(i)}']
                    sets = request.POST[f'sets-{str(i)}']
                    weight = request.POST[f'weight-{str(i)}']
                    comment = request.POST[f'comment-{str(i)}']

                    workout_exercise = WorkoutExercise()
                    workout_exercise.personal_workout = new_training
                    workout_exercise.exercise = Exercise.objects.get(id=exercise_id)
                    workout_exercise.sets = sets
                    workout_exercise.weight = weight
                    workout_exercise.comment = comment

                    workout_exercise.save()

            elif request.POST['training-type'] == 'general':
                new_training = GeneralWorkout()
                new_training.title = request.POST['title']
                new_training.visibility = request.POST['visible-radio'] == 'yes'
                new_training.save()

                # Add exercises
                row_count = int(request.POST['rowCount'])
                for i in range(1, row_count + 1):
                    exercise_id = request.POST[f'exercise-{str(i)}']
                    sets = request.POST[f'sets-{str(i)}']
                    weight = request.POST[f'weight-{str(i)}']
                    comment = request.POST[f'comment-{str(i)}']

                    workout_exercise = WorkoutExercise()
                    workout_exercise.general_workout = new_training
                    workout_exercise.exercise = Exercise.objects.get(id=exercise_id)
                    workout_exercise.sets = sets
                    workout_exercise.weight = weight
                    workout_exercise.comment = comment

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
    return render(request, 'show_training.html',
                  {'training': personal_training, 'workout_exercises': workout_exercises})


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

        # Add exercises
        row_count = int(request.POST['rowCount'])
        for i in range(1, row_count + 1):
            exercise_id = request.POST[f'exercise-{str(i)}']
            sets = request.POST[f'sets-{str(i)}']
            weight = request.POST[f'weight-{str(i)}']
            comment = request.POST[f'comment-{str(i)}']

            workout_exercise = WorkoutExercise()
            workout_exercise.general_workout = training
            workout_exercise.exercise = Exercise.objects.get(id=exercise_id)
            workout_exercise.sets = sets
            workout_exercise.weight = weight
            workout_exercise.comment = comment

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

        # Add exercises
        row_count = int(request.POST['rowCount'])
        for i in range(1, row_count + 1):
            exercise_id = request.POST[f'exercise-{str(i)}']
            sets = request.POST[f'sets-{str(i)}']
            weight = request.POST[f'weight-{str(i)}']
            comment = request.POST[f'comment-{str(i)}']

            workout_exercise = WorkoutExercise()
            workout_exercise.personal_workout = training
            workout_exercise.exercise = Exercise.objects.get(id=exercise_id)
            workout_exercise.sets = sets
            workout_exercise.weight = weight
            workout_exercise.comment = comment

            workout_exercise.save()

        training.save()
        return redirect('show_training')

    return render(request, 'edit_training.html',
                  {'training': training,
                   'workout_exercises': workout_exercises,
                   'exercises': exercises,
                   'clients': clients}
                  )


@login_required
@csrf_protect
def delete_general_training(request, id):
    general_training = GeneralWorkout.objects.get(id=id)
    workout_exercises = WorkoutExercise.objects.filter(general_workout=general_training)

    for workout_exercise in workout_exercises:
        workout_exercise.delete()

    general_training.delete()

    return redirect('show_training')


@login_required
@csrf_protect
def delete_personal_training(request, id):
    personal_training = PersonalWorkout.objects.get(id=id)
    workout_exercises = WorkoutExercise.objects.filter(personal_workout=personal_training)

    for workout_exercise in workout_exercises:
        workout_exercise.delete()

    personal_training.delete()

    return redirect('show_training')


@login_required
def show_tags(request):
    muscle_tags = MuscleTag.objects.all()
    exercise_type_tags = ExerciseTypeTag.objects.all()
    return render(request, 'show_tags.html', {'muscle_tags': muscle_tags, 'exercise_type_tags': exercise_type_tags})


@login_required
def show_tag(request, tag_type, id):
    if tag_type == 'muscle':
        tag = MuscleTag.objects.get(id=id)
    elif tag_type == 'exercise-type':
        tag = ExerciseTypeTag.objects.get(id=id)
    else:
        return redirect('show_tags')
    return render(request, 'show_tag.html', {'tag': tag, 'tag_type': tag_type})


@login_required
@csrf_protect
def add_tag(request):
    if request.method == 'POST':
        tag_type = request.POST['tag-type']
        if tag_type == 'muscle-tag':
            new_muscle_tag = MuscleTag()
            new_muscle_tag.name = request.POST['name']
            new_muscle_tag.save()

            if request.FILES:
                image = request.FILES['image']

                if image:
                    md5 = hashlib.md5()
                    for chunk in image.chunks():
                        md5.update(chunk)
                    file_hash = md5.hexdigest()

                    extension = os.path.splitext(image.name)[1]
                    new_name = f"{file_hash}{extension}"
                    image.name = new_name

                    new_muscle_tag.image = image
            new_muscle_tag.save()

        elif tag_type == 'exercise-type-tag':
            new_exercise_type_tag = ExerciseTypeTag()
            new_exercise_type_tag.name = request.POST['name']
            new_exercise_type_tag.save()

            if request.FILES:
                image = request.FILES['image']

                if image:
                    md5 = hashlib.md5()
                    for chunk in image.chunks():
                        md5.update(chunk)
                    file_hash = md5.hexdigest()

                    extension = os.path.splitext(image.name)[1]
                    new_name = f"{file_hash}{extension}"
                    image.name = new_name

                    new_exercise_type_tag.image = image

            new_exercise_type_tag.save()

        return redirect('show_tags')

    return render(request, 'add_tag.html')


@login_required
@csrf_protect
def edit_tag(request, tag_type, id):
    if tag_type == 'muscle':
        tag = MuscleTag.objects.get(id=id)
    elif tag_type == 'exercise-type':
        tag = ExerciseTypeTag.objects.get(id=id)
    else:
        return redirect('show_tags')

    if request.method == 'POST':
        tag.name = request.POST['name']

        if request.FILES:
            file = request.FILES['image']

            if file:
                md5 = hashlib.md5()
                for chunk in file.chunks():
                    md5.update(chunk)
                file_hash = md5.hexdigest()

                extension = os.path.splitext(file.name)[1]
                new_name = f"{file_hash}{extension}"
                file.name = new_name

                tag.image.delete()
                tag.image = file

        tag.save()
        return redirect('show_tags')

    return render(request, 'edit_tag.html', {'tag': tag, 'tag_type': tag_type})


@login_required
def delete_tag(request, tag_type, id):
    if tag_type == 'muscle':
        tag = MuscleTag.objects.get(id=id)
        tag.image.delete()
        tag.delete()
    elif tag_type == 'exercise-type':
        tag = ExerciseTypeTag.objects.get(id=id)
        tag.image.delete()
        tag.delete()
    return redirect('show_tags')


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
def edit_client(request, id):
    client = Person.objects.get(id=id)
    if request.method == 'POST':
        client.first_name = request.POST['first_name']
        client.last_name = request.POST['last_name']
        client.email = request.POST['email']
        client.status = request.POST['status']

        if request.POST["password"] != '':
            client.set_password(request.POST['password'])

        if request.FILES:
            file = request.FILES['photo']

            if file:
                md5 = hashlib.md5()
                for chunk in file.chunks():
                    md5.update(chunk)
                file_hash = md5.hexdigest()

                extension = os.path.splitext(file.name)[1]
                new_name = f"{file_hash}{extension}"
                file.name = new_name

                # Delete old photo
                client.photo.delete()
                client.photo = file

        client.save()
        return redirect('show_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'edit_client.html', {'client': client, 'form': form})


@login_required
def show_clients(request):
    clients = Person.objects.exclude(status='hidden')
    return render(request, 'show_clients.html', {"clients": clients})


@login_required
def show_client(request, id):
    client = Person.objects.get(id=id)
    return render(request, 'show_client.html', {'client': client})


@login_required
def delete_client(request, id):
    client = Person.objects.get(id=id)
    if not client.is_staff:
        client.status = 'hidden'
        client.save()
    return redirect('show_clients')


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
