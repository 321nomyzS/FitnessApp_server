from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ExerciseViewSet, GeneralWorkoutViewSet, PersonalWorkoutViewSet, WorkoutExerciseViewSet)


router = DefaultRouter()
router.register(r'exercise', ExerciseViewSet)
router.register(r'generalworkout', GeneralWorkoutViewSet)
router.register(r'personalworkout', PersonalWorkoutViewSet)
router.register(r'workoutexercise', WorkoutExerciseViewSet)


urlpatterns = [
    path('', include(router.urls)),
]