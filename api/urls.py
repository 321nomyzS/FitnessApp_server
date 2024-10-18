from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet)
router.register(r'generalworkout', GeneralWorkoutViewSet)
router.register(r'personalworkout', PersonalWorkoutViewSet)
router.register(r'muscletag', MuscleTagViewSet)
router.register(r'exercisetypetag', ExerciseTypeTagViewSet)
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'currentuser', CurrentUserView, basename='currentuser')


urlpatterns = [
    path('', include(router.urls)),
]
