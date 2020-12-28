from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the games index.")

def create(request):
    return HttpResponse("You want to create a game")

def join(request, game_id):
    return HttpResponse("Joining game %s." % game_id)