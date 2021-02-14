from django import forms

class GuessForm(forms.Form):
    guess = forms.CharField(label='Guess', max_length=64, required=False)

class CreateGameForm(forms.Form):
    username = forms.CharField(label='Name', max_length=64, required=True)

class JoinGameForm(forms.Form):
    code = forms.CharField(label='Code', max_length=5, required=True)
    username = forms.CharField(label='Name', max_length=64, required=True)
    