from django.shortcuts import render, redirect
from .models import *
from .utils import *

# Create your views here.

def home(request):
    return render(request, 'trackerapp/home.html')

def exercises(request):
    exercises = Exercise.objects.all().order_by('name')
    
    return render(request, 'trackerapp/exercises/exercises.html', {'exercises': exercises})

def add_exercise(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')

        try:
            ExerciseOperations.create_exercise(name, category)
            return redirect('exercises')
        except ValueError:
            # Optional: handle invalid form data
            pass

    return render(request, 'trackerapp/exercises/add_exercise.html')

def update_exercise(request, exercise_id):
    try:
        exercise = ExerciseOperations.get_exercise_by_id(exercise_id)
    except Exercise.DoesNotExist:
        return redirect('exercise_list')

    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        ExerciseOperations.update_exercise(exercise_id, name, category)
        return redirect('exercises')

    return render(request, 'trackerapp/exercises/update_exercise.html', {'exercise': exercise})

def delete_exercise(request, exercise_id):
    if request.method == 'POST':
        ExerciseOperations.delete_exercise(exercise_id)

    return redirect('exercises')
