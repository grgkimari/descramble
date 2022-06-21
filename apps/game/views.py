from .models import HighScore
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
        addCookie = False
        incrementCookie = False
        score = None
        #check if there is a previously stored cookie and assign score
        if 'score' in request.COOKIES:
            score = int(request.COOKIES.get('score'))
        else:
            score = 0
        form = AttemptForm(request.POST)
        if form.is_valid():
            
            previous_attempt = Attempt.objects.all()[0]
            previous_attempt.attemptText = form.cleaned_data.get('attemptText')
            previous_attempt.save()
            if previous_attempt.attemptText == previous_attempt.word:
                message = "Correct!"
                if request.user.is_authenticated:
                    #score tracking for registered users
                    #fix currentscore not resetting
                    request.user.currentScore += 1
                    request.user.save()
                    highscores = [highscore for highscore in HighScore.objects.filter(user = request.user).order_by('score')]
                    if len(highscores) > 0:
                        if request.user.currentScore > highscores[0].score or len(highscores) < 10:
                            newHighScore = HighScore.objects.create(score = request.user.currentScore, user = request.user)
                            newHighScore.save()
                            if len(highscores) == 10:
                                highscores[0].delete()
                    else:
                        newHighScore = HighScore.objects.create(score = request.user.currentScore, user = request.user)
                        newHighScore.save()
                else:
                    #Score tracking for unregistered users
                    if 'score' in request.COOKIES:
                        score += 1
                        incrementCookie = True
                    else:
                        score = 1
                        addCookie = True
            else:
                message = "Incorrect. Your attempt was " + previous_attempt.attemptText + ". The correct word is " + previous_attempt.word
                if 'score' not in request.COOKIES:
                    score = 0
                    addCookie = True
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
        highscores = None
        if request.user.is_authenticated:
            highscores = [highscore for highscore in HighScore.objects.filter(user = request.user)]
        response = render(request, 'game/homepage.html', {'score' : score, 'highscores' : highscores, 'form' : form1, 'word' : word, 'scrambled_word' : scrambled_word, 'message' : message})
        if addCookie:
            response.set_cookie('score', score, max_age=3600)
            return response
        elif incrementCookie:
            response.delete_cookie('score')
            response.set_cookie('score', score)
            return response
        else:
            return response
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