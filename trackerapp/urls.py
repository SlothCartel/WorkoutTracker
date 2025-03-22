from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('exercises/', views.exercises, name='exercises'),
    path('exercises/add/', views.add_exercise, name='add_exercise'),
    path('exercises/<int:exercise_id>/update/', views.update_exercise, name='update_exercise'),
    path('exercises/<int:exercise_id>/delete/', views.delete_exercise, name='delete_exercise'),
    path('workouts/', views.workouts, name='workouts'),
    path('workouts/<int:workout_id>/', views.view_workout, name='view_workout'),
    path('workouts/add/', views.add_workout, name='add_workout'),
    path('workouts/<int:workout_id>/update/', views.update_workout, name='update_workout'),
    path('workouts/<int:workout_id>/delete/', views.delete_workout, name='delete_workout'),
]