from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import date


def exercise_directory_path(instance, filename):
    return f'exercise/{instance.id}/{filename}'


def client_directory_path(instance, filename):
    return f'client/{instance.id}/{filename}'


class ExerciseType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


class ExerciseLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    language_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)


class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    image = models.ImageField(upload_to=exercise_directory_path, blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    html_content = models.TextField()
    type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)
    language = models.ForeignKey(ExerciseLanguage, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class GeneralWorkout(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    exercises = models.ManyToManyField('Exercise', through='WorkoutExercise')
    visibility = models.BooleanField()

    def __str__(self):
        return f"General Workout #{self.pk}"


class WorkoutExercise(models.Model):
    id = models.AutoField(primary_key=True)
    general_workout = models.ForeignKey('GeneralWorkout', on_delete=models.CASCADE, null=True, blank=True)
    personal_workout = models.ForeignKey('PersonalWorkout', on_delete=models.CASCADE, null=True, blank=True)
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.exercise.title} in {self.personal_workout} or {self.general_workout}"


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=client_directory_path, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('active_until', 'Active until specific date')
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    active_until = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def is_active(self):
        if self.status == 'active':
            return True
        elif self.status == 'active_until' and self.active_until >= date.today():
            return True
        return False


class PersonalWorkout(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    exercises = models.ManyToManyField('Exercise', through='WorkoutExercise')
    visibility = models.BooleanField()
    workout_date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Personal Workout on {self.workout_date}"