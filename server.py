import collections as coll
import json
import math
import uuid

from datetime import datetime as dt
from pprint import pprint

from flask import Flask, request

app = Flask(__name__)

receipts = coll.defaultdict(str)

@app.route("/", methods=['GET'])
def home():
    return '<h1>Hello.</h1>'

@app.route("/receipts/process", methods=['POST'])
def process():
    receipt = json.loads(request.data)
    pprint(receipt)
    
    # out of scope: account for duplicate receipts posted
    while True:
        receipt_id = str(uuid.uuid4())
        if receipt_id not in receipts:
            break

    receipts[receipt_id] = receipt
    return {'id': receipt_id}

@app.route("/receipts/<id>/points", methods=['GET'])
def get_points(id: str):
    if id not in receipts:
        raise ValueError(f'receipt {id} not found - cannot calculate points')

    receipt = receipts[id]
    pprint(receipt)
    points = 0

    # One point for every alphanumeric character in the retailer name.
    retailer = receipt['retailer']
    for letter in retailer:
        if letter.isalnum():
            points += 1
    print (f'added {points} points for retailer name')
    
    # 50 points if the total is a round dollar amount with no cents.
    total = receipt['total']
    if float(total).is_integer():
        points += 50
        print ('added 50 points because total is a round dollar amount')
        
    # 25 points if the total is a multiple of 0.25.
    if float(total) % 0.25 == 0:
        points += 25
        print ('added 25 points because total is multiple of 0.25')
        
    # 5 points for every two items on the receipt.
    items = receipt['items']
    every_two_items = len(items) // 2
    points += every_two_items * 5
    print (f'added {every_two_items * 5} total for every 2 items')
    
    # If the trimmed length of the item description is a multiple of 3, 
    # multiply the price by 0.2 and round up to the nearest integer. 
    # The result is the number of points earned.
    for item in items:
        if len(item['shortDescription'].strip()) % 3 == 0:
            v = math.ceil(float(item['price']) * 0.2)
            points += v
            print (f'added {v} point(s) for item description length')

    # 6 points if the day in the purchase date is odd.
    date = receipt['purchaseDate']
    time = receipt['purchaseTime']
    date_with_time = f'{date} {time}'
    dt_converted = dt.strptime(date_with_time, '%Y-%m-%d %H:%M')
    if dt_converted.day % 2 != 0:
        points += 6
        print ('added 6 points for odd purchase date')
    
    # 10 points if the time of purchase is after 2:00pm 
    # and before 4:00pm.
    if dt_converted.hour >= 14 and dt_converted.hour <= 16:
        points += 10
        print ('added 10 points for purchase time between 2 and 4 pm')
    
    return {'points': points}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)