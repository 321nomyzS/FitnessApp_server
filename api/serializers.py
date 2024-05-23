from rest_framework import serializers
from trener.models import Exercise, GeneralWorkout, PersonalWorkout, WorkoutExercise, Person
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


class PersonalWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalWorkout
        fields = '__all__'


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'comment']  # Tu dodajesz 'comment' do serializowanych pól


class GeneralWorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(source='workoutexercise_set', many=True, read_only=True)

    class Meta:
        model = GeneralWorkout
        fields = ['id', 'title', 'visibility', 'exercises']