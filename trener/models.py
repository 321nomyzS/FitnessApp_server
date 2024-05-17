from django.db import models
from django.core.validators import FileExtensionValidator
import os


def exercise_directory_path(instance, filename):
    return f'exercise/{instance.id}/{filename}'


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


class PersonalWorkout(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    exercises = models.ManyToManyField('Exercise', through='WorkoutExercise')
    visibility = models.BooleanField()
    workout_date = models.DateField()

    def __str__(self):
        return f"Personal Workout on {self.workout_date}"


class WorkoutExercise(models.Model):
    id = models.AutoField(primary_key=True)
    general_workout = models.ForeignKey('GeneralWorkout', on_delete=models.CASCADE, null=True, blank=True)
    personal_workout = models.ForeignKey('PersonalWorkout', on_delete=models.CASCADE, null=True, blank=True)
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.exercise.title} in {self.personal_workout} or {self.general_workout}"