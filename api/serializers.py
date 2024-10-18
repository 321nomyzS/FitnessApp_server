from trener.models import *
from rest_framework import serializers
from django.contrib.auth import authenticate


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')

        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        attrs['user'] = user
        return attrs

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
        fields = ['exercise', 'comment', 'tempo', 'rest_min', 'rest_sec', 'warmup_series', 'main_series',
                  'main_series_reps', 'warmup_series_1_rep', 'warmup_series_2_rep', 'warmup_series_3_rep',
                  'main_series_1_rep', 'main_series_2_rep', 'main_series_3_rep', 'main_series_4_rep', 'alter_exercise']


class PersonalWorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(source='workoutexercise_set', many=True, read_only=True)

    class Meta:
        model = PersonalWorkout
        fields = '__all__'


class GeneralWorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(source='workoutexercise_set', many=True, read_only=True)

    class Meta:
        model = GeneralWorkout
        fields = '__all__'


class MuscleTagSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = MuscleTag
        fields = '__all__'


class ExerciseTypeTagSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = ExerciseTypeTag
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'message', 'rating', 'personal_workout', 'exercise', 'person', 'date']
        read_only_fields = ['id', 'person', 'date']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'status', 'active_until', 'email', 'first_name', 'last_name', 'photo']
        read_only_fields = ['id', 'status', 'active_until', 'photo']

