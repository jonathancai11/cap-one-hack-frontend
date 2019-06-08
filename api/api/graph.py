import json
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import pandas

dining = set(['KFC','City Dogs', 'McDonalds', 'Panda Express', 'Chick-Fil-A', 'EL TACO', 'urban Farmhouse market & care', 'Cookout', 'Steak Shake'])

def diningGraph():
    with open('data/history.json') as json_file:
        history = json.load(json_file)['transactions']
    
    monthData = [[0] * 7 for i in range(2)]
    for transaction in history:
        if transaction['vendor'] in dining:
            day = datetime.strptime(transaction["date"],"%m/%d/%Y").weekday()
            month = datetime.strptime(transaction["date"],"%m/%d/%Y").month
            if month == 4:
                monthData[0][day] += transaction["totalCost"]
            else:
                monthData[1][day] += transaction["totalCost"]
    
    df = pandas.DataFrame(dict(graph= ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
                                n= monthData[0][:], m= monthData[1][:]))
    ind = np.arange(len(df))
    width = 0.4

    fig, ax = plt.subplots()
    ax.barh(ind, df.n, width, color='red', label='April')
    ax.barh(ind + width, df.m, width, color='green', label='May')

    ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
    ax.legend()

    plt.title('Dining')
    plt.show()

def getTotal():
    with open('data/history.json') as json_file:
        history = json.load(json_file)['transactions']

    total = [0]*2

    for transaction in history:
        month = datetime.strptime(transaction["date"],"%m/%d/%Y").month
        if month == 4:
            total[0] += transaction["totalCost"]
        else:
            total[1] += transaction["totalCost"]
    
    print(total)
        

getTotal()
