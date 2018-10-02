from flask import render_template, flash, redirect
from app import app

# index view function suppressed for brevity


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Power'}  # fake user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'fdsfdsfds'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'fdsfdsfds'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
posts=posts)
