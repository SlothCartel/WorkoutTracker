from django.shortcuts import render, redirect
from .models import *
from .utils import *
import json
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder

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

def workouts(request):
    workouts = Workout.objects.all().order_by('date')

    return render(request, 'trackerapp/workouts/workouts.html', {'workouts': workouts})

def view_workout(request, workout_id):
    try:
        workout = WorkoutOperations.get_workout_by_id(workout_id)
    except Workout.DoesNotExist:
        return redirect('workouts')

    return render(request, 'trackerapp/workouts/view_workout.html', {'workout': workout})

def add_workout(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        notes = request.POST.get('notes')
        exercise_ids = request.POST.getlist('exercise_ids')

        # Call backend logic
        WorkoutOperations.create_workout(request.POST, date, notes, exercise_ids)
        return redirect('workouts')

    all_exercises = Exercise.objects.all().order_by('name')
    return render(request, 'trackerapp/workouts/add_workout.html', {'all_exercises': all_exercises})

def update_workout(request, workout_id):
    workout = WorkoutOperations.get_workout_by_id(workout_id)

    if request.method == 'POST':
        date = request.POST.get('date')
        notes = request.POST.get('notes')
        exercise_ids = request.POST.getlist('exercise_ids')

        WorkoutOperations.update_workout(request.POST, workout, date, notes, exercise_ids)
        return redirect('workouts')

    all_exercises = Exercise.objects.all().order_by('name')
    current_exercise_ids = list(workout.exercises.values_list('exercise_id', flat=True))

    # Build prefill data
    exercise_form_data = {}
    for we in workout.exercises.all():
        if we.exercise.category == 'WEIGHT':
            sets = list(Set.objects.filter(workout_exercise=we).values('reps', 'weight'))
            exercise_form_data[str(we.exercise.id)] = {'sets': sets}
        elif we.exercise.category == 'CARDIO':
            try:
                cardio = CardioLog.objects.get(workout_exercise=we)
                exercise_form_data[str(we.exercise.id)] = {
                    'duration': int(cardio.duration_minutes) if cardio.duration_minutes is not None else '',
                    'distance': float(cardio.distance_km) if cardio.distance_km is not None else '',
                    'calories': int(cardio.calories_burned) if cardio.calories_burned is not None else '',
                }   
            except CardioLog.DoesNotExist:
                pass

    return render(request, 'trackerapp/workouts/update_workout.html', {
        'workout': workout,
        'all_exercises': all_exercises,
        'current_exercise_ids': current_exercise_ids,
        'exercise_form_data_json': json.dumps(exercise_form_data, cls=DjangoJSONEncoder),
    })


def delete_workout(request, workout_id):
    if request.method == 'POST':
        workout = WorkoutOperations.get_workout_by_id(workout_id)
        workout.delete()

    return redirect('workouts')