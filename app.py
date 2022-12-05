from flask import Flask,jsonify,request

app = Flask(__name__)


tasks = [
    {
        'id':1,
        'title':u'Buy Groceries',
        'description':u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done':False
    },
    {
        'id':2,
        'title':u'Learn Python',
        'description':u'Need to find a good Python tutorial on the web',
        'done':False
    }
]




