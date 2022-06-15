from email import message
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import AttemptForm
from .models import Attempt
import json
import random
import logging

logging.basicConfig(filename='descramble_game.log', format='%(Pastime)s %(msg)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def getWord():
    with open('F:/Projects/Dev/django_projects/descramble_venv/descramble_project/apps/game/words.json') as allWordFile:
        data = json.load(allWordFile)
        allWordFile.close()
        searchValue = random.randint(0,len(data) - 1)
        while True:  
            for item in data.items():
                if item[1] == searchValue:
                    word = item[0]
        wordList = [letter for letter in word]
        scrambled_word = ''
        for i in range(len(word)):
            index =random.randint(0,len(wordList)-1)
            scrambled_word = scrambled_word + wordList[index]
            wordList.remove(wordList[index])
        return (word,scrambled_word,data)


def homePage(request):
    message = None
    id = None
    form = AttemptForm()

    if request.method == 'POST':
        word,scrambled_word,data = getWord()
        form1 = AttemptForm(request.POST)
        form = AttemptForm()
        attempt = Attempt.objects.create(word = word,attemptText = '--NONE--')
        attempt.save()
        
        id = request.COOKIES['id']
        previous_attempt = Attempt.objects.get(id = id)
        if form1.is_valid():
            previous_attempt.attemptText = form1.cleaned_data.get('attemptText')
            previous_attempt.save()
            if previous_attempt.word == previous_attempt.attemptText:
                message = "Correct !"
            else:
                message = "Not Correct! The word was " + previous_attempt.word + ". Your attempt was " + previous_attempt.attemptText
            previous_attempt.delete()
        else:
            message = 'form is invalid'

        response = render(request, 'game/homepage.html', {'form' : form, 'word' : word, 'scrambled_word' : scrambled_word, 'message' : message})

        if 'message' in request.COOKIES:
            response.delete_cookie('message')
        if 'id' in request.COOKIES:
            response.cookies['id'] = attempt.id
        else:
            response.set_cookie('id', attempt.id)
        return response
    else:
        word,scrambled_word,data = getWord()
        form = AttemptForm()
        attempt = Attempt.objects.create(word = word,attemptText = '--NONE--')
        attempt.save()
        response = render(request, 'game/homepage.html', {'form' : form, 'word' : word, 'scrambled_word' : scrambled_word, 'message' : message})
        if 'message' in request.COOKIES:
            response.delete_cookie('message')
        if 'id' in request.COOKIES:
            response.cookies['id'] = attempt.id
        else:
            response.set_cookie('id', attempt.id)
        return response