from django.urls import path
import trener.views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('plant/add/', views.add_plant, name='add_plant'),
    path('exercise', views.show_exercises, name='show_exercise'),
    path('exercise/<id>', views.show_exercise, name='show_exercise'),
    path('delete_exercise/<id>/', views.delete_exercise, name='delete_exercise'),
    path('edit_exercise/<id>/', views.edit_exercise, name='edit_exercise'),
    path('training/add', views.add_training, name='add_training'),
    path('training', views.show_training, name='show_training'),
    path('training/general/<id>', views.show_general_training, name='show_general_training'),
    path('training/personal/<id>', views.show_personal_training, name='show_personal_training'),
    path('training/general/edit/<id>', views.edit_general_training, name='edit_general_training'),
    path('training/personal/edit/<id>', views.edit_personal_training, name='edit_personal_training'),
    path('client/add', views.add_client, name='add_client'),
    path('client', views.show_clients, name='show_clients'),
    path('client/<id>', views.show_client, name='show_client'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_tunnel, name='logout_tunnel'),
    path('plant/delete/<int:id>/', views.delete_plant, name='delete_plant'),
    path('plants/', views.show_plants, name='show_plants'),
    path('plant/<int:id>/', views.show_plant, name='show_plant'),
    path('plant/edit/<int:id>/', views.edit_plant, name='edit_plant'),
]
