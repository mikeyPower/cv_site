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
    return render_template("index.html")



@app.route('/result',methods = ['POST', 'GET'])
def result():
   form = ContactForm()

   if request.method == 'POST':
        result = request.form
        for k,v in result.items():
            print(v)
            #check if string is empty
            if not v.strip():
                flash('All fields are required.')
                print("flash")
                return redirect(url_for('index',_anchor='contact'))
        print("Your message has been sent")
        flash('Your message was sent, thank you!')
        return redirect(url_for('index',_anchor='contact'))

   elif request.method == 'GET':
       return render_template("index.html")


#Build a scrapper for the quotes section of the site to change it everyday
