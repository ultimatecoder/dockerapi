from flask import Flask
app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome to Flask based webclient of Docker!'
