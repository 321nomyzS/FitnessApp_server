from rest_framework import viewsets
from .serializers import (ExerciseSerializer, ExerciseTypeSerializer, GeneralWorkoutSerializer, PersonalWorkoutSerializer, WorkoutExerciseSerializer)
from trener.models import Exercise, ExerciseType, GeneralWorkout, PersonalWorkout, WorkoutExercise, Person
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



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

class ExerciseTypeListView(APIView):
    def get(self, request):
        categories = ExerciseType.objects.all()
        serializer = ExerciseTypeSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)