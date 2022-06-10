from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import AttemptForm
import json
import random
import csv
from pconst import const

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
def storeWord(word,id):
    row = (word,id)
    with open('wordsSent.csv','w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(row)

def getStoredWord(id):
    with open('wordsSent.csv','r') as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            if int(line[1]) == id:
                return line[0]

def incrementId():
    with open('id.txt','r+') as f:
        id = int(f.readline())
        id = id+1
        f.seek(0)
        f.truncate()
        f.write(str(id))

def getId():
    with open('id.txt','r') as f:
        id = int(f.readline())
        return id

def resultPage(request):
    attemptText = None
    word,scrambled_word,data= getWord()
    storeWord(word,getId())
    messages.success(request,"After function call word = "+ word)
    form = AttemptForm()
    messages.success(request,"After form render word = " + word)
    if request.method == 'POST':
        messages.success(request,"Before form post word = " + word)
        form = AttemptForm(request.POST)
        messages.success(request,"After form post word = " + word)
        if form.is_valid():        
            attemptText = form.cleaned_data.get('attemptText').strip()
            
            if attemptText == word:
                messages.success(request, "Correct!")
            elif len(attemptText) == len(word) and attemptText in data:
                messages.success(request,"Not the word we were looking for! The word was " + getStoredWord(getId()))
            else:
                messages.error(request,"Wrong! The word was " + getStoredWord(getId()) + str(getId()))
            incrementId()
        return redirect('homePage')
    return render(request,'game/homepage.html',{'form' : form, 'data' : data, 'scrambled_word' : scrambled_word, 'id' : getId()})


def homePage(request):
    attemptText = None
    word,scrambled_word,data= getWord()
    storeWord(word,getId()-1)
    messages.success(request,"After function call word = "+ word)
    form = AttemptForm()
    messages.success(request,"After form render word = " + word)
    if request.method == 'POST':
        messages.success(request,"Before form post word = " + word)
        form = AttemptForm(request.POST)
        messages.success(request,"After form post word = " + word)
        if form.is_valid():        
            attemptText = form.cleaned_data.get('attemptText').strip()
            
            if attemptText == word:
                messages.success(request, "Correct!")
            elif len(attemptText) == len(word) and attemptText in data:
                messages.success(request,"Not the word we were looking for! The word was " + getStoredWord(getId()))
            else:
                messages.error(request,"Wrong! The word was " + getStoredWord(getId()) + str(getId()))
            incrementId()
        return resultPage(request)
    return render(request,'game/homepage.html',{'form' : form, 'data' : data, 'scrambled_word' : scrambled_word, 'id' : getId()})