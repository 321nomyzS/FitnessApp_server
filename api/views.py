from rest_framework import viewsets, status
from .serializers import *
from trener.models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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


class FeedbackViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        # Automatyczne przypisanie zalogowanego użytkownika jako 'person'
        serializer.save(person=self.request.user)

    def create(self, request, *args, **kwargs):
        # Możliwość modyfikacji odpowiedzi na stworzenie feedbacku
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Feedback successfully created!", "data": response.data}, status=status.HTTP_201_CREATED)