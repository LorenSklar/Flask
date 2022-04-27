# My version of Hello World:

from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return "Hello World, it's me Flask!"

@app.route('/bye')
def bye_world():
    return "Buh bye!"

@app.route('/new')
def new_world():
    return "I am a shiny new Flask..."
