from rest_framework import viewsets
from .serializers import *
from trener.models import *
from rest_framework.authentication import TokenAuthentication
from trener.models import Exercise
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })


class ExerciseViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = Exercise.objects.filter(id__gte=1)
    serializer_class = ExerciseSerializer


class GeneralWorkoutViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = GeneralWorkout.objects.filter(visibility=True)
    serializer_class = GeneralWorkoutSerializer


class PersonalWorkoutViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = PersonalWorkout.objects.all()
    serializer_class = PersonalWorkoutSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(client=user)


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer


class MuscleTagViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = MuscleTag.objects.all()
    serializer_class = MuscleTagSerializer


class ExerciseTypeTagViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = ExerciseTypeTag.objects.all()
    serializer_class = ExerciseTypeTagSerializer
