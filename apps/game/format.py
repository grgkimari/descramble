import json

with open('F:/Projects/Dev/django_projects/descramble_venv/descramble_project/apps/game/words.json', 'r+') as allWordFile:
    data = json.load(allWordFile)
    for item in data.items():
        print(type(item))
        break
