from rest_framework import serializers
from trener.models import Exercise, GeneralWorkout, PersonalWorkout, WorkoutExercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


class GeneralWorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = GeneralWorkout
        fields = ['id', 'title', 'visibility', 'exercises']


class PersonalWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalWorkout
        fields = '__all__'


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = '__all__'
