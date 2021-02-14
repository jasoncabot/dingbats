import logging

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.forms import formset_factory
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError

from .models import Game, PuzzleSelection, PlayerGuess, Player, Puzzle
from .forms import *

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'game/home.html')


def index(request):
    games = Game.objects.order_by('created_at')[:5]
    context = {'games': games}
    return render(request, 'game/index.html', context)


def create_game():
    game = Game()
    while not game.id:
        game.regenerate_code()
        try:
            game.save()
        except IntegrityError:
            logger.info('Tried to save game with code ' +
                        game.code + ' but couldnt')
    return game


def new_game(request):
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game = create_game()
            player = game.player_set.create(name=form.cleaned_data['username'])
            request.session['player_' + str(game.id)] = player.id
            # TODO: Make these puzzles a random shuffle from 0-count(puzzles)
            puzzles = Puzzle.objects.all()[:15]
            for order, item in enumerate(puzzles):
                game.selected.create(sort_key=order, puzzle=item)
            return HttpResponseRedirect(reverse('detail', args=[game.id]))
    else:
        form = CreateGameForm()

    return render(request, 'game/new.html', {'form': form})


def join_game(request):
    if request.method == 'POST':
        form = JoinGameForm(request.POST)
        if form.is_valid():
            game = Game.objects.get(
                code=form.cleaned_data['code'].upper(), state=Game.State.CREATED)
            player = game.player_set.create(name=form.cleaned_data['username'])
            request.session['player_' + str(game.id)] = player.id
            return HttpResponseRedirect(reverse('detail', args=[game.id]))
    else:
        form = JoinGameForm()

    return render(request, 'game/join.html', {'form': form})


def detail(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game does not exist")

    players = game.player_set.order_by('created_at').all()

    if not 'player_' + str(game.id) in request.session:
        raise PermissionDenied
    try:
        me = players.get(id=request.session['player_' + str(game.id)])
    except Player.DoesNotExist:
        raise PermissionDenied

    selections = game.selected.select_related(
        'puzzle').order_by('sort_key').all().prefetch_related('guesses__player')
    puzzles = [s.puzzle for s in selections]

    def guessed_correctly(player, puzzle): return player in [
        guess.player for guess in puzzle.guesses.all()]
    guesses = [[(player, guessed_correctly(player, s))
                for player in players] for s in selections]

    GuessFormSet = formset_factory(GuessForm, extra=0)
    initial = [{} for _ in puzzles]
    forms = GuessFormSet(initial=initial) if request.method == 'GET' else GuessFormSet(
        request.POST, initial=initial)

    context = {
        'game': game,
        'me': me,
        'puzzles': zip(puzzles, guesses, forms),
        'management_form': forms.management_form
    }

    if request.method == 'GET':  # View a game
        return render(request, 'game/detail.html', context)
    elif request.method == 'POST':  # Submit a guess
        if forms.is_valid():
            for idx, form in enumerate(forms):
                guess = form.cleaned_data['guess'].lower()
                correct = puzzles[idx].answers.filter(value=guess).count() != 0
                if correct:
                    selections[idx].guesses.create(player=me)

        return HttpResponseRedirect('')
    else:
        return HttpResponse("Must GET or POST")
