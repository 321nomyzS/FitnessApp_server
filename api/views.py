from rest_framework import viewsets
from .serializers import (ExerciseSerializer, GeneralWorkoutSerializer, PersonalWorkoutSerializer, WorkoutExerciseSerializer)
from trener.models import ExerciseType, ExerciseLanguage, Exercise, GeneralWorkout, PersonalWorkout, WorkoutExercise, Client


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class GeneralWorkoutViewSet(viewsets.ModelViewSet):
    queryset = GeneralWorkout.objects.filter(visibility=True)
    serializer_class = GeneralWorkoutSerializer


class PersonalWorkoutViewSet(viewsets.ModelViewSet):
    queryset = PersonalWorkout.objects.all()
    serializer_class = PersonalWorkoutSerializer


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer
