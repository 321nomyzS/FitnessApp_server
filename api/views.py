from rest_framework import viewsets
from .serializers import (ExerciseSerializer, GeneralWorkoutSerializer, PersonalWorkoutSerializer, WorkoutExerciseSerializer)
from trener.models import Exercise, GeneralWorkout, PersonalWorkout, WorkoutExercise, Person
from rest_framework.permissions import IsAuthenticated


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class GeneralWorkoutViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = GeneralWorkout.objects.filter(visibility=True)
    serializer_class = GeneralWorkoutSerializer


class PersonalWorkoutViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = PersonalWorkout.objects.all()
    serializer_class = PersonalWorkoutSerializer

    def get_queryset(self):
        return self.queryset.filter(client=self.request.user)


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer
