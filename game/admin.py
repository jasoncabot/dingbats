from django.contrib import admin

from .models import Puzzle, CorrectAnswer, Game, Player, PuzzleSelection, PlayerGuess

admin.site.register(Puzzle)
admin.site.register(CorrectAnswer)
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(PuzzleSelection)
admin.site.register(PlayerGuess)
