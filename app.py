from flask import Flask,render_template
import os
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signin")
def signin():
    return render_template('signin.html')

if __name__=="__main__":
    app.run(debug=True,port=8000)