from django.contrib import admin
from .models import Person, PersonalWorkout, GeneralWorkout, MuscleTag, ExerciseTypeTag, Exercise

admin.site.register(Person)
admin.site.register(PersonalWorkout)
admin.site.register(GeneralWorkout)
admin.site.register(MuscleTag)
admin.site.register(ExerciseTypeTag)
admin.site.register(Exercise)
