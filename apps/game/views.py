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
    

    response = None
    message = None
    id = None
    if request.method == 'POST':
        form = AttemptForm(request.POST)
        word,scrambled_word,data = getWord()
        if 'message' in request.COOKIES:
            message = request.COOKIES['message']
        if 'id' in request.COOKIES:
            id = request.COOKIES['id']
        if form.is_valid():
            attempt = Attempt.objects.create(word = word)
            attempt.attemptText = form.cleaned_data.get('attemptText')
            attempt.save()
            response = render(request, 'game/homepage.html',{'word' : attempt.word, 'scrambled_word' : scrambled_word, 'form' : form, 'message' : message})
            if attempt.word.strip() == attempt.attemptText.strip():
                response.set_cookie('message', 'Correct!')
                response.set_cookie('id', str(attempt.id))
                
            else:
                response.set_cookie('message', 'Wrong! The correct word was ' + attempt.word + ' Your attempt was ' + attempt.attemptText)
                response.set_cookie('id', str(attempt.id))
            attempt.isChecked = False
            return response
        else:
            message = 'Form is not valid'
            response = render(request, 'game/homepage.html',{'word' : attempt.word, 'scrambled_word' : scrambled_word, 'form' : form, 'message' : message})
            return response
    else:
        form = AttemptForm()
        word,scrambled_word,data = getWord()
        response = render(request, 'game/homepage.html',{'word' : word, 'scrambled_word' : scrambled_word, 'form' : form, 'message' : message })
        logger.debug(str(response))
        return response