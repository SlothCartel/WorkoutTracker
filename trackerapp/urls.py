from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('exercises/', views.exercises, name='exercises'),
    path('exercises/add/', views.add_exercise, name='add_exercise'),
    path('exercises/<int:exercise_id>/update/', views.update_exercise, name='update_exercise'),
    path('exercises/<int:exercise_id>/delete/', views.delete_exercise, name='delete_exercise'),
]