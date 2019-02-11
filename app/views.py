from flask import render_template, flash, redirect, request, Flask, url_for
from app import app
from forms import ContactForm

from flask_mail import Mail
import re
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
   mail = Mail(app)
   form = ContactForm()

   if request.method == 'POST':
        result = request.form
        for k,v in result.items():
            print(k,v)
            if k == "contactEmail":
                print("contact email")
                if valid_email(v) == False:
                    flash('Email is not correct')
                    return redirect(url_for('index',_anchor='contact'))
            #check if string is empty
            if not v.strip():
                flash('All fields are required.')
                print("flash")
                return redirect(url_for('index',_anchor='contact'))
        print("Your message has been sent")

        msg = Message(recipients=result["contactEmail"],
                    sender="powerm3@tcd.ie",
                      body=result["contactMessage"],
                      subject=result["contactSubject"])

        mail.send(msg)



        flash('Your message was sent, thank you!')
        return redirect(url_for('index',_anchor='contact'))

   elif request.method == 'GET':
       return render_template("index.html")




def valid_email(input_email):
    email = input_email
    if re.match("\A(?P<name>[\w\-_]+)@(?P<domain>[\w\-_]+).(?P<toplevel>[\w]+)\Z",email,re.IGNORECASE):
        return True
    #print("Email is valid")
    else:
        return False
    #print("Email is invalid")

#Build a scrapper for the quotes section of the site to change it everyday
