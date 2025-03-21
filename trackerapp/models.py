from django.db import models

# Create your models here.
class ExerciseCategory(models.TextChoices):
    WEIGHT = 'WEIGHT', 'Weight Training'
    CARDIO = 'CARDIO', 'Cardio'

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=ExerciseCategory.choices)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Workout(models.Model):
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Workout on {self.date}"
    
class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.exercise.name} in workout {self.workout.date}"
    
class Set(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name='sets')
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # e.g. 90.50kg

    def __str__(self):
        return f"{self.reps} reps @ {self.weight}kg"
    
class CardioLog(models.Model):
    workout_exercise = models.OneToOneField(WorkoutExercise, on_delete=models.CASCADE, related_name='cardio_log')
    duration_minutes = models.PositiveIntegerField()
    distance_km = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    calories_burned = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.duration_minutes} min of {self.workout_exercise.exercise.name}"