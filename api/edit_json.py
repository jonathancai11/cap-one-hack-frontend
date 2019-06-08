import json

with open('demo.json') as json_file:
    data = json.load(json_file)

with open('history.json') as json_file_hist:
    hist = json.load(json_file_hist)

hist.append(data[0])
print(hist)