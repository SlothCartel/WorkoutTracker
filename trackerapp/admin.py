from django.contrib import admin
from .models import Exercise, Workout, WorkoutExercise, Set, CardioLog

# Register your models here.
class SetInline(admin.TabularInline):
    model = Set
    extra = 1

class CardioLogInline(admin.StackedInline):
    model = CardioLog
    extra = 0
    max_num = 1

class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'workout')
    inlines = [SetInline, CardioLogInline]

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('date', 'notes')
    inlines = [WorkoutExerciseInline]

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(WorkoutExercise, WorkoutExerciseAdmin)