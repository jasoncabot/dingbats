import uuid
from django.db import models
from django.utils.crypto import get_random_string


def upload_location(instance, filename):
    _, extension = filename.split('.')
    return 'puzzles/%s.%s' % (str(uuid.uuid4()), extension)


def create_new_code(length):
    return get_random_string(length).upper()


class Puzzle(models.Model):
    photo = models.ImageField(upload_to=upload_location)
    description = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.description


class CorrectAnswer(models.Model):
    puzzle = models.ForeignKey(
        Puzzle, on_delete=models.CASCADE, related_name='answers')
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.value

    def save(self, force_insert=False, force_update=False):
        self.value = self.value.lower()
        super(CorrectAnswer, self).save(force_insert, force_update)


class Game(models.Model):
    class State(models.IntegerChoices):
        CREATED = 1
        STARTED = 2
        ENDED = 3

    code = models.CharField(max_length=5, default=create_new_code(5))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.PositiveSmallIntegerField(
        choices=State.choices, default=State.CREATED)

    def regenerate_code(self):
        self.code = create_new_code(5)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(fields=['code'], condition=models.Q(
                state=1), name='unique_code_game')
        ]


class Player(models.Model):
    name = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

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
