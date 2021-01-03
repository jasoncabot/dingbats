from django.http import HttpResponse, Http404
from django.shortcuts import render

from .models import Game, PuzzleSelection, PlayerGuess, Player


def index(request):
    games = Game.objects.order_by('created_at')[:5]
    context = {'games': games}
    return render(request, 'game/index.html', context)


def detail(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game does not exist")

    players = game.player_set.all()
    puzzles = [(selection.puzzle, selection.guesses.select_related('player').all())
               for selection in game.selected.select_related('puzzle').order_by('sort_key').all()]
    context = {
        'game': game,
        'players': players,
        'puzzles': puzzles
    }

    if request.method == 'GET':  # View a game
        return render(request, 'game/detail.html', context)
    elif request.method == 'POST':  # Submit a guess
        return HttpResponse("POST ")
    else:
        return HttpResponse("Must GET or POST")
