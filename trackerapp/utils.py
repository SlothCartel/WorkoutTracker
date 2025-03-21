from .models import *

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
        