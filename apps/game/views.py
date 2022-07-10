from urllib import response
from .models import HighScore
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import AttemptForm
from .models import Attempt
import json
import random

#get word from json file
def getWord(level):
    word = None
    with open('static/game/words.json') as allWordFile:
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
        lives = None
        addCookie = False
        changeScoreCookie = False
        score = None
        message = None
        changeLives = False
        setLivesCookie = False
        #check for the number of lives
        if 'lives' in request.COOKIES:
            lives = int(request.COOKIES.get('lives'))
        else:
            setLivesCookie = True
            lives = 3

        #check if there is a previously stored cookie and assign score
        if 'score' in request.COOKIES:
            score = int(request.COOKIES.get('score'))
        else:
            score = 0
        form = AttemptForm(request.POST)
        if request.user.is_authenticated:
            word, scrambled_word, data = getWord(request.user.level)
        else:
             word, scrambled_word, data = getWord("Very Easy")
        if form.is_valid():
            
            previous_attempt = Attempt.objects.all()[0]
            previous_attempt.attemptText = form.cleaned_data.get('attemptText')
            previous_attempt.save()
            if previous_attempt.attemptText == previous_attempt.word:
                message = "Correct!"
                if request.user.is_authenticated:
                    #score tracking for registered users
                    request.user.currentScore += 5
                    request.user.save()
                else:
                    #Score tracking for unregistered users
                    if 'score' in request.COOKIES:
                        score += 5
                        changeScoreCookie = True
                    else:
                        score = 5
                        addCookie = True
            elif len(previous_attempt.word) == len(previous_attempt.attemptText) and list(previous_attempt.attemptText).sort() == list(previous_attempt.word).sort() and previous_attempt.attemptText in data.keys():
                message = '\'' + previous_attempt.attemptText + '\' ' + "is an English word but not the word we were looking for. The word was " + previous_attempt.word
                if request.user.is_authenticated:
                    #update user's currentScore and save
                    request.user.currentScore += 3
                    request.user.save()
                    
                else:
                    message = previous_attempt.attemptText + " is an English word but not the word we were looking for. The correct word is " + previous_attempt.word
                     #Score tracking for unregistered users
                    if 'score' in request.COOKIES:
                        score += 3
                        changeScoreCookie = True
                    else:
                        score = 3
                        addCookie = True
            else:
                lives -= 1
                message = "Incorrect. Your attempt was " + previous_attempt.attemptText + ". The correct word is " + previous_attempt.word
                if 'score' not in request.COOKIES:
                    score = 0
                    addCookie = True
                    
                if lives not in request.COOKIES:
                    changeLives = True

            Attempt.objects.all().delete()

        else:
            message = "Form is not valid"

        
        attempt = Attempt.objects.create(word=word, attemptText = "--NONE--")
        attempt.save()
        form1 = AttemptForm()
        highscores = None
        isNewHighScore = False
        achievedScore = None

        if lives <= 0:
            lives = 3
            #get HighScores and update if score is a high score
            if request.user.is_authenticated:
                achievedScore = request.user.currentScore
                highscores = [highscore for highscore in HighScore.objects.filter(user = request.user).order_by('score')]
                if len(highscores) > 0:
                    if request.user.currentScore > highscores[0].score or len(highscores) < 10:
                        isNewHighScore = True
                        newHighScore = HighScore.objects.create(score = request.user.currentScore, user = request.user)
                        newHighScore.save()
                        if len(highscores) == 10:
                            highscores[0].delete()
                
                # create highscore if none        
                else:
                    newHighScore = HighScore.objects.create(score = request.user.currentScore, user = request.user)
                    newHighScore.save()
                request.user.currentScore = 0
                request.user.save()
            else:
                
                achievedScore = score
                score = 0
                changeScoreCookie = True
                changeLives = True

            response = render(request, 'game/game_over.html', {'score' : achievedScore, 'isNewHighScore' : isNewHighScore})
            if  changeLives:
                response.set_cookie('lives', str(lives))
            if changeScoreCookie:
                response.set_cookie('score', score)
            return response
        if request.user.is_authenticated:
            highscores = [highscore for highscore in HighScore.objects.filter(user = request.user)]
        response = render(request, 'game/homepage.html', {'lives' : lives, 'score' : score, 'highscores' : highscores, 'form' : form1, 'word' : word, 'scrambled_word' : scrambled_word, 'message' : message})
        if changeLives:
            response.set_cookie('lives', str(lives))
        if addCookie:
            response.set_cookie('score', score, max_age=3600)
            return response
        elif changeScoreCookie:
            response.set_cookie('score', score)
            return response
        else:
            return response
    else:
        #if form is not submitted
        form = AttemptForm()
        message = "Welcome to descramble"
        lives = None

            
        if request.user.is_authenticated:
            word, scrambled_word, data = getWord(request.user.level)
            attempt = Attempt.objects.create(word=word, attemptText = "--NONE--")
            attempt.save()
        else:
            word, scrambled_word, data = getWord("Very Easy")
            attempt = Attempt.objects.create(word=word, attemptText = "--NONE--")
            attempt.save()

        response = render(request, 'game/homepage.html', {'form' : form, 'word' : word, 'scrambled_word' : scrambled_word, 'message' : message})
        setLivesCookie = False

        if 'lives' in request.COOKIES:
            lives = int(request.COOKIES.get('lives'))
        else:
            setLivesCookie = True
            lives = 3

        response = render(request, 'game/homepage.html', {'lives' : lives, 'form' : form, 'word' : word, 'scrambled_word' : scrambled_word, 'message' : message})

        if setLivesCookie:
            response.set_cookie('lives', '3')
        return response 
