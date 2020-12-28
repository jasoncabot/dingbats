from django.contrib import admin

from .models import Puzzle, CorrectAnswer

admin.site.register(Puzzle)
admin.site.register(CorrectAnswer)