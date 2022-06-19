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

def getWord(level):
    word = None
    with open('words.json') as allWordFile:
        minWordLength = maxWordLength = 0
        if level == "Very Easy":
            minWordLength = 3
            maxWordLength = 4
        elif level == "Easy":
            minWordLength = 4
            maxWordLength = 5
        elif level == "Medium":
            minWordLength = 5
            maxWordLength = 6
        elif level == "Hard":
            minWordLength = 7
            maxWordLength = 12
        elif level == "Very Hard":
            minWordLength = 12
            maxWordLength = 16
        elif level == "Legendary":
            minWordLength = 20
            maxWordLength = 50
            
        data = json.load(allWordFile)
        allWordFile.close()
        cont = True

        while cont: 
            searchValue = random.randint(0,len(data) - 1)
            for item in data.items():
                if item[1] == searchValue:
                    word = item[0]
                    if len(word) >= minWordLength and len(word) <= maxWordLength:
                        cont = False
                        break
                    
                
        wordList = [letter for letter in word]
        scrambled_word = ''
        for i in range(len(word)):
            index =random.randint(0,len(wordList)-1)
            scrambled_word = scrambled_word + wordList[index]
            wordList.remove(wordList[index])
        return (word,scrambled_word,data)

def homePage(request):
    if request.method == 'POST':
        message = None
        form = AttemptForm(request.POST)
        if form.is_valid():
            
            previous_attempt = Attempt.objects.all()[0]
            previous_attempt.attemptText = form.cleaned_data.get('attemptText')
            previous_attempt.save()
            if previous_attempt.attemptText == previous_attempt.word:
                message = "Correct!"
            else:
                message = "Incorrect. Your attempt was " + previous_attempt.attemptText + ". The correct word is " + previous_attempt.word
            
            Attempt.objects.all().delete()

        else:
            message = "Form is not valid"

        if request.user.is_authenticated:
            word, scrambled_word, data = getWord(request.user.level)
        else:
             word, scrambled_word, data = getWord("Very Easy")
        
        attempt = Attempt.objects.create(word=word, attemptText = "--NONE--")
        attempt.save()
        form1 = AttemptForm()

        return render(request, 'game/homepage.html', {'form' : form1, 'word' : word, 'scrambled_word' : scrambled_word, 'message' : message})
    else:
        form = AttemptForm()
        message = "Welcome to descramble"
        if request.user.is_authenticated:
            word, scrambled_word, data = getWord(request.user.level)
            attempt = Attempt.objects.create(word=word, attemptText = "--NONE--")
            attempt.save()
        else:
            word, scrambled_word, data = getWord("Very Easy")
            attempt = Attempt.objects.create(word=word, attemptText = "--NONE--")
            attempt.save()
        return render(request, 'game/homepage.html', {'form' : form, 'word' : word, 'scrambled_word' : scrambled_word, 'message' : message})