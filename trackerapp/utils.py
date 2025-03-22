from .models import *
from django.db.models import Count
from django.db.models import Sum, F, FloatField
from django.db.models.functions import TruncWeek
from datetime import datetime, timedelta
from datetime import datetime, timedelta

class ExerciseOperations:

    @staticmethod
    def create_exercise(name: str, category: str) -> Exercise:
        if not name or not category:
            raise ValueError('Name and category are required')
        
        return Exercise.objects.create(name=name, category=category)
    
    @staticmethod
    def get_all_exercises():
        return Exercise.objects.all().order_by('name')
    
    @staticmethod
    def get_exercise_by_id(exercise_id: int):
        return Exercise.objects.get(id=exercise_id)
    
    @staticmethod
    def update_exercise(exercise_id: int, name: str, category: str):
        exercise = Exercise.objects.get(id=exercise_id)
        exercise.name = name
        exercise.category = category
        exercise.save()
        return exercise
    
    @staticmethod
    def delete_exercise(exercise_id: int):
        exercise = Exercise.objects.get(id=exercise_id)
        exercise.delete()

class WorkoutOperations:

    @staticmethod
    def create_workout(post_data, date, notes, exercise_ids):
        if not date or not exercise_ids:
            raise ValueError("Date and at least one exercise are required.")

        workout = Workout.objects.create(date=date, notes=notes)

        for exercise_id in exercise_ids:
            exercise = Exercise.objects.get(id=exercise_id)
            workout_exercise = WorkoutExercise.objects.create(
                workout=workout,
                exercise=exercise
            )

            if exercise.category == 'WEIGHT':
                reps_list = post_data.getlist(f'weight_{exercise_id}_reps[]')
                weight_list = post_data.getlist(f'weight_{exercise_id}_weight[]')

                for reps, weight in zip(reps_list, weight_list):
                    Set.objects.create(
                        workout_exercise=workout_exercise,
                        reps=int(reps),
                        weight=float(weight)
                    )

            elif exercise.category == 'CARDIO':
                duration = post_data.get(f'cardio_{exercise_id}_duration')
                distance = post_data.get(f'cardio_{exercise_id}_distance')
                calories = post_data.get(f'cardio_{exercise_id}_calories')

                CardioLog.objects.create(
                    workout_exercise=workout_exercise,
                    duration_minutes=int(duration) if duration else 0,
                    distance_km=float(distance) if distance else None,
                    calories_burned=int(calories) if calories else None
                )

        return workout
    
    @staticmethod
    def get_all_workouts():
        return Workout.objects.all().order_by('date')
    
    @staticmethod
    def get_workout_by_id(workout_id: int):
        return Workout.objects.get(id=workout_id)
    
    @staticmethod
    def update_workout(post_data, workout, date, notes, exercise_ids):
        workout.date = date
        workout.notes = notes
        workout.save()

        # Delete removed exercises
        existing_links = WorkoutExercise.objects.filter(workout=workout)
        for we in existing_links:
            if str(we.exercise.id) not in exercise_ids:
                we.delete()

        # Track which exercise_ids are already linked
        existing_exercise_ids = set(existing_links.values_list('exercise_id', flat=True))

        # Loop through selected exercises
        for exercise_id in exercise_ids:
            exercise = Exercise.objects.get(id=exercise_id)

            # Get or create WorkoutExercise
            we, created = WorkoutExercise.objects.get_or_create(
                workout=workout,
                exercise=exercise
            )

            if exercise.category == 'WEIGHT':
                # Clear old sets
                Set.objects.filter(workout_exercise=we).delete()

                reps_list = post_data.getlist(f'weight_{exercise_id}_reps[]')
                weight_list = post_data.getlist(f'weight_{exercise_id}_weight[]')

                for reps, weight in zip(reps_list, weight_list):
                    Set.objects.create(
                        workout_exercise=we,
                        reps=int(reps),
                        weight=float(weight)
                    )

            elif exercise.category == 'CARDIO':
                # Delete old cardio log if exists
                CardioLog.objects.filter(workout_exercise=we).delete()

                duration = post_data.get(f'cardio_{exercise_id}_duration')
                distance = post_data.get(f'cardio_{exercise_id}_distance')
                calories = post_data.get(f'cardio_{exercise_id}_calories')

                if duration:
                    CardioLog.objects.create(
                        workout_exercise=we,
                        duration_minutes=int(duration),
                        distance_km=float(distance) if distance else None,
                        calories_burned=int(calories) if calories else None
                    )
    
    @staticmethod
    def delete_workout(workout_id: int):
        workout = Workout.objects.get(id=workout_id)
        workout.delete()

class HomeOperations:

    @staticmethod
    def get_top_exercises(limit=3):
        #Returns the top most frequently performed exercises
        #based on how many workout records they appear in
        
        exercise_counts = WorkoutExercise.objects.values('exercise__id', 'exercise__name') \
            .annotate(count=Count('exercise')) \
            .order_by('-count')[:limit]

        top_exercises = [
        {
            'name': item['exercise__name'],
            'count': item['count']
        }
        for item in exercise_counts
        ]
        
        return top_exercises

    @staticmethod
    def get_weekly_weight_volume(weeks=10):
        #Calculate weekly weight training volume (weight * reps)

        start_date = datetime.now().date() - timedelta(weeks=weeks)

        weekly_data = {}

        workouts = Workout.objects.filter(date__gte=start_date).order_by('date')

        for workout in workouts:
            week_key = workout.date.strftime('%b %d')
            
            if week_key not in weekly_data:
                weekly_data[week_key] = 0
            
            weight_exercises = WorkoutExercise.objects.filter(
                workout=workout,
                exercise__category='WEIGHT'
            )

        for we in weight_exercises:
                sets = Set.objects.filter(workout_exercise=we)
                for s in sets:
                    weekly_data[week_key] += float(s.weight) * s.reps

        sorted_weeks = sorted(weekly_data.keys(), key=lambda x: datetime.strptime(x, '%b %d'))

        return {
            'labels': sorted_weeks,
            'data': [weekly_data[week] for week in sorted_weeks]
        }
    
    @staticmethod
    def get_weekly_cardio_volume(weeks=10):
        #Calculate weekly cardio volume

        start_date = datetime.now().date() - timedelta(weeks=weeks)

        weekly_data = {}

        workouts = Workout.objects.filter(date__gte=start_date).order_by('date')

        for workout in workouts:
            week_key = workout.date.strftime('%b %d')
            
            if week_key not in weekly_data:
                weekly_data[week_key] = 0
            
            cardio_exercises = WorkoutExercise.objects.filter(
                workout=workout,
                exercise__category='CARDIO' 
        )

        for we in cardio_exercises:
            try:
                cardio = CardioLog.objects.get(workout_exercise=we)
                
                volume = cardio.duration_minutes
                
                if cardio.distance_km:
                    volume += float(cardio.distance_km) * 5
                
                if cardio.calories_burned:
                    volume += cardio.calories_burned / 10
                
                weekly_data[week_key] += volume
            except CardioLog.DoesNotExist:
                pass  

        sorted_weeks = sorted(weekly_data.keys(), key=lambda x: datetime.strptime(x, '%b %d'))

        return {
            'labels': sorted_weeks,
            'data': [weekly_data[week] for week in sorted_weeks]
        }