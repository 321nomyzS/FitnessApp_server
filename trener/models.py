from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import date
from django.contrib.auth.models import AbstractUser


def exercise_directory_path(instance, filename):
    return f'exercise/{instance.id}/{filename}'


def person_directory_path(instance, filename):
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

from django.db import models

class WaterNeed(models.Model):
    name = models.CharField(max_length=100, verbose_name="Potrzeba wody")
    description = models.TextField(verbose_name="Opis", blank=True)

    def __str__(self):
        return self.name

class LightRequirement(models.Model):
    name = models.CharField(max_length=100, verbose_name="Wymagania świetlne")
    description = models.TextField(verbose_name="Opis", blank=True)

    def __str__(self):
        return self.name

class CareLevel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Poziom pielęgnacji")
    description = models.TextField(verbose_name="Opis", blank=True)

    def __str__(self):
        return self.name

class Plant(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nazwa")
    description = models.TextField(verbose_name="Opis")
    image = models.ImageField(upload_to='images/', verbose_name="Zdjęcie")
    water_need = models.ForeignKey(WaterNeed, on_delete=models.CASCADE, verbose_name="Potrzeba wody")
    light_requirement = models.ForeignKey(LightRequirement, on_delete=models.CASCADE, verbose_name="Wymagania świetlne")
    care_level = models.ForeignKey(CareLevel, on_delete=models.CASCADE, verbose_name="Poziom pielęgnacji")
    is_indoor = models.BooleanField(default=True, verbose_name="Do uprawy wewnątrz")

    def __str__(self):
        return self.name


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


class Person(AbstractUser):
    plants = models.ManyToManyField(Plant, related_name='owners')
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to=person_directory_path, blank=True, null=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('active_until', 'Active until specific date')
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    active_until = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
    client = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f"Personal Workout on {self.workout_date}"