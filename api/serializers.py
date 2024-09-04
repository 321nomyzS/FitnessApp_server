from rest_framework import serializers
from trener.models import Exercise, GeneralWorkout, ExerciseType, PersonalWorkout, WorkoutExercise, Person
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate
from trener.models import Person
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('email', 'password', 'first_name', 'last_name', 'status', 'active_until')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Person.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            status=validated_data['status'],
            active_until=validated_data['active_until'],
        )
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'comment']


class PersonalWorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(source='workoutexercise_set', many=True, read_only=True)

    class Meta:
        model = PersonalWorkout
        fields = ['id', 'title', 'visibility', 'workout_date', 'client', 'exercises']


class GeneralWorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(source='workoutexercise_set', many=True, read_only=True)

    class Meta:
        model = GeneralWorkout
        fields = ['id', 'title', 'visibility', 'exercises']


class ExerciseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseType
        fields = ['id', 'type_name']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'photo', 'status', 'active_until']