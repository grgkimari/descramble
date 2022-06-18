import  json

with open('words.json', 'r+') as f:
    data = json.load(f)
    data2 = data
    count = 0
    for item in data.items():
        print(len(item[0]))
        break
print("___________________SUCCESS_______________________")