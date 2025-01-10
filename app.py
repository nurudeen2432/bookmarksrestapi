#This imports the Flask class from the flask
from flask import Flask, jsonify

# creates an instance of the Flask class.
app = Flask(__name__)

#route decorator using app.get instead of app.route
@app.get("/")
def index():
    return "Hello World"



@app.get("/hello")
def hello():
    return jsonify({"message":"Hello world"})


# if(__name__) == '__main__':
#              app.run()