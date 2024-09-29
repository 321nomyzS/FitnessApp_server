from rest_framework import viewsets
from .serializers import (PersonSerializer, ExerciseSerializer, ExerciseTypeSerializer, GeneralWorkoutSerializer, PersonalWorkoutSerializer, WorkoutExerciseSerializer)
from trener.models import Exercise, ExerciseType, GeneralWorkout, PersonalWorkout, WorkoutExercise, Person
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from trener.models import Person
from rest_framework_simplejwt.views import TokenBlacklistView
from trener.models import Exercise

class BlacklistTokenUpdateView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    queryset = Person.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer




class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class GeneralWorkoutViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = GeneralWorkout.objects.filter(visibility=True)
    serializer_class = GeneralWorkoutSerializer


class PersonalWorkoutViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = PersonalWorkout.objects.all()
    serializer_class = PersonalWorkoutSerializer

    def get_queryset(self):
        return self.queryset.filter(client=1)


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer

class ExerciseTypeListView(APIView):
    def get(self, request):
        categories = ExerciseType.objects.all()
        serializer = ExerciseTypeSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PersonSerializer(user)
        return Response(serializer.data)