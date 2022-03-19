from flask import Flask, render_template

app = Flask(__name__)


# @app.route('/')  # app route or URL only "/" means it will open in home page
# def hello_world():
#   return '<h1> hello world </h1>'


@app.route('/about')  # to make about page
def about_page():
    return '<h1> About page </h1>'


@app.route('/about/<username>')  # to open about page for different users
def user_page(username):
    return f'<h1> multi user about page  this is about page of {username}</h1>'


@app.route('/')  # app route or URL only "/" means it will open in home page
@app.route('/home')
def homepage():
    return render_template('home.html')


@app.route('/features')
def feature():
    return render_template('feature.html')
