from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'This is the home page'

@app.route('Hello')
def hello():
    return 'Hello'
