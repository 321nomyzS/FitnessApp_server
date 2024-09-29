from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ExerciseViewSet, GeneralWorkoutViewSet,
                    PersonalWorkoutViewSet, WorkoutExerciseViewSet, ExerciseTypeListView, BlacklistTokenUpdateView, UserProfileView)
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenBlacklistView, TokenObtainPairView,
    TokenVerifyView,)


router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet)
router.register(r'generalworkout', GeneralWorkoutViewSet)
router.register(r'personalworkout', PersonalWorkoutViewSet)
router.register(r'workoutexercise', WorkoutExerciseViewSet)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('exercise-types/', ExerciseTypeListView.as_view(), name='exercise-type-list'),
    path('', include(router.urls)),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
]