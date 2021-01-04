import uuid
from django.db import models


def upload_location(instance, filename):
    _, extension = filename.split('.')
    return 'puzzles/%s.%s' % (str(uuid.uuid4()), extension)


class Puzzle(models.Model):
    photo = models.ImageField(upload_to=upload_location)
    description = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.description


class CorrectAnswer(models.Model):
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.value


class Game(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class State(models.IntegerChoices):
        CREATED = 1
        STARTED = 2
        ENDED = 3
    state = models.PositiveSmallIntegerField(
        choices=State.choices, default=State.CREATED)

    def __str__(self):
        return self.name + " (" + self.get_state_display() + ")"

    class Meta:
        ordering = ['created_at']


class Player(models.Model):
    name = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PuzzleSelection(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="selected")
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    sort_key = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['sort_key']

    def __str__(self):
        return f'{self.game}: {self.sort_key} - {self.puzzle}'


class PlayerGuess(models.Model):
    puzzle_selection = models.ForeignKey(
        PuzzleSelection, on_delete=models.CASCADE, related_name="guesses")
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Player guesses"

    def __str__(self):
        return f'{self.puzzle_selection} - {self.player.name}'
