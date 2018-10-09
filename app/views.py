from flask import render_template, flash, redirect, request, Flask
from app import app
from forms import ContactForm

# index view function suppressed for brevity


@app.route('/')
@app.route('/index')
def index():

    return render_template("index.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      return 'Form posted.'

  elif request.method == 'GET':
    return render_template('contact.html', form=form)


#Build a scrapper for the quotes section of the site to change it everyday
