from flask import render_template, flash, redirect, request, Flask, url_for
from app import app
from forms import ContactForm

# index view function suppressed for brevity
#app = Flask(__name__)

#app.secret_key = 'development key'

@app.route('/',methods=['GET', 'POST'])
@app.route('/index')
def index():
    #form = ContactForm()
    #print("Your in the contact section")
    #return render_template("index.html",form=form)
     form = ContactForm()
     print("Your in the contact section")
     if request.method == 'POST':
       if form.validate() == False:
         flash('All fields are required.')
         print("flash")
         return redirect(url_for('index',_anchor='contact'))
         #return render_template("index.html")
       else:
         flash('Your message was sent, thank you!')
         return redirect(url_for('index',_anchor='contact'))

     elif request.method == 'GET':
         return render_template("index.html",form=form)

@app.route('/contact1', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
  print("Your in the contact section")
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      print("flash")
      return redirect(url_for('contact'))
      #return render_template("contact1.html")
    else:
      return 'Form posted.'

  elif request.method == 'GET':
      return render_template("contact1.html",form=form)
    #return redirect(url_for('/'))


#Build a scrapper for the quotes section of the site to change it everyday
