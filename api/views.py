from rest_framework import viewsets, status, generics
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
    http_method_names = ['get']


class GeneralWorkoutViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = GeneralWorkout.objects.filter(visibility=True)
    serializer_class = GeneralWorkoutSerializer
    http_method_names = ['get']


class PersonalWorkoutViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = PersonalWorkout.objects.all()
    serializer_class = PersonalWorkoutSerializer
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(client=user)


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer
    http_method_names = ['get']


class MuscleTagViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = MuscleTag.objects.all()
    serializer_class = MuscleTagSerializer
    http_method_names = ['get']


class ExerciseTypeTagViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = ExerciseTypeTag.objects.all()
    serializer_class = ExerciseTypeTagSerializer
    http_method_names = ['get']


class FeedbackViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    http_method_names = ['post']

    def perform_create(self, serializer):
        serializer.save(person=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Feedback successfully created!", "data": response.data}, status=status.HTTP_201_CREATED)


class CurrentUserView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(id=user.id)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
