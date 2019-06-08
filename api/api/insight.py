import json
from collections import Counter
from collections import OrderedDict 
from datetime import datetime

vendor_cat = {
    "DINING": {'KFC','City Dogs', 'McDonalds', 'Panda Express', 'Chick-Fil-A', 'EL TACO', 'urban Farmhouse market & care', 'Cookout', 'Steak Shake'},
    "GROCERY": {'Farm Fresh','CVS Pharmarcy', 'Walmart'},
    "ENTERTAINMENT": {'Regal Theatre'},
    "ELECTRONIC": {'Amazon','Best Buy', },
    "UTILITIES": {'Dominion','Richmond Water','Richmond Gas Works', 'Comcast'},
    "RENT": {'Rent'}
}

weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

def insight_dates(json_file):
    with open(json_file) as readJSON:
        data = json.load(readJSON, object_hook= _byteify)["transactions"]

    dateCost = [0]*7

    for transaction in data:
        if transaction["vendor"] in vendor_cat["DINING"]:
            day = datetime.strptime(transaction["date"],"%m/%d/%Y").weekday()
            dateCost[day] += round(transaction["totalCost"],2)

    aList = list()
    for index, dates in enumerate(weekday):
        aDict = dict()
        aDict["day"] = dates
        aDict["cost"]= str(dateCost[index])
        aList.append(aDict)
    return aList 

def insight_categories(json_file):
    with open(json_file) as readJSON:
        data = json.load(readJSON, object_hook= _byteify)["transactions"]

    cost_cat = dict()
    for vendor in vendor_cat:
        cost_cat[vendor] = 0

    for transaction in data:
        for vendor in vendor_cat:
            if transaction["vendor"] in vendor_cat[vendor]:
                cost_cat[vendor] += round(transaction["totalCost"],2)

    aList = list()
    for category, cost in cost_cat.items():
        aDict = dict()
        aDict["vendor"] = category
        aDict["cost"] = str(cost)
        aList.append(aDict)
    return aList

def insight_vendors(json_file):
    Vendor = {} 
    with open(json_file) as json_file:
        data = json.load(json_file, object_hook= _byteify)["transactions"]
    for transaction in data:
        if transaction["vendor"] in Vendor:
            Vendor[transaction["vendor"]] += 1
        else:
            Vendor[transaction["vendor"]] = 1
        
    aList = list()
    for vendor, nBills in Vendor.items():
        aDict = dict()
        aDict["vendor"] = vendor
        aDict["nBills"] = str(nBills)
        aList.append(aDict)
    return aList

def insight_specific_categories(json_file):
    with open(json_file) as readJSON:
        data = json.load(readJSON, object_hook= _byteify)["transactions"]

    specific_cat = dict()
    return_dict = dict()
    for vendor in vendor_cat:
        specific_cat[vendor] = {}
        return_dict[vendor] = OrderedDict()

    for transaction in data:
        for vendor in vendor_cat:
            if transaction["vendor"] in vendor_cat[vendor]:
                for item in transaction["items"]:
                    if item["item"] not in specific_cat[vendor]:
                        specific_cat[vendor][item["item"]] = round(float(item["cost"]) * int(item["quantity"]), 2)
                    else:
                        specific_cat[vendor][item["item"]] += round(float(item["cost"]) * int(item["quantity"]), 2)

    for category in specific_cat:
        c = Counter(specific_cat[category])
        for tuple_category in c.most_common():
            return_dict[category][tuple_category[0]] = str(tuple_category[1])
    
    aList = list()
    for category, order_dict in return_dict.items():
        aDict = dict()
        aDict["category"] = category
        aDict["orderItems"] = order_dict
        aList.append(aDict)
    
    return aList

def make_insight_json(json_file):
    aDict = dict()
    aDict["categories"] = insight_categories(json_file)
    aDict["vendors"] = insight_vendors(json_file)
    aDict["dates"] = insight_dates(json_file)
    aDict["specific_cat"] = insight_specific_categories(json_file)
    aDict["subscriptions"] = {
        "monthly" : 
            [
                {
                    "service" : "Netflix",
                    "cost" : '10.00'
                },
                {
                    "service" : "Hulu",
                    "cost" : '5.00'
                },
                {
                    "service" : "Apple Music",
                    "cost" : '5.00'
                }
            ],
        "yearly" :
            [
                {
                    "service" : "Xbox Live Gold Membership",
                    "cost" : '50.00'
                }
            ]
    }
    return {
        "insights": aDict
    }

def make_month(json_file):
    with open(json_file) as readJSON:
        data = json.load(readJSON, object_hook= _byteify)["transactions"]
    
    aMonth = {}

    month_str = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug','Sep','Oct','Nov','Dec']

    for transaction in data:
        month = month_str[datetime.strptime(transaction["date"],"%m/%d/%Y").month - 1]
        if month in aMonth:
            aMonth[month].append(transaction)
        else:
            aMonth[month] = [transaction]
    return {
        "transaction": aMonth
    }