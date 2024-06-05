from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ExerciseViewSet, GeneralWorkoutViewSet,
                    PersonalWorkoutViewSet, WorkoutExerciseViewSet)
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


router = DefaultRouter()
router.register(r'exercise', ExerciseViewSet)
router.register(r'generalworkout', GeneralWorkoutViewSet)
router.register(r'personalworkout', PersonalWorkoutViewSet)
router.register(r'workoutexercise', WorkoutExerciseViewSet)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]