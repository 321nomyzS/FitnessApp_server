from django.urls import path
import trener.views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('exercise/add', views.add_exercise, name='add_exercise'),
    path('exercise', views.show_exercises, name='show_exercise'),
    path('exercise/<id>', views.show_exercise, name='show_exercise'),
    path('training/add', views.add_training, name='add_training'),
    path('training', views.show_training, name='show_training'),
    path('training/general/<id>', views.show_general_training, name='show_general_training'),
    path('training/personal/<id>', views.show_personal_training, name='show_personal_training'),
]