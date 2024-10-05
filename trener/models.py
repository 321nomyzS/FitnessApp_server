import hashlib
import os
from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models


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


class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    html_content = models.TextField()
    type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)
    language = models.ForeignKey(ExerciseLanguage, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = Exercise.objects.get(pk=self.pk)

                if old_instance.image and self.image != old_instance.image:
                    old_instance.image.delete(save=False)
            except Exercise.DoesNotExist:
                pass

        if self.image:
            file = self.image
            md5 = hashlib.md5()

            for chunk in file.chunks():
                md5.update(chunk)
            file_hash = md5.hexdigest()

            extension = os.path.splitext(file.name)[1]
            new_name = f"{self.id}/{file_hash}{extension}"

            self.image.name = os.path.join('exercise', new_name)

        super().save(*args, **kwargs)


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
    sets = models.TextField(blank=True, null=True)
    weight = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.exercise.title} in {self.personal_workout} or {self.general_workout}"


class Person(AbstractUser):
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to=person_directory_path, blank=True, null=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('active_until', 'Active until specific date'),
        ('hidden', 'Hidden')
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
