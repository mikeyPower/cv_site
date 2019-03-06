from flask import render_template, flash, redirect, request, Flask, url_for
#from app import app
from forms import ContactForm

from flask_mail import Mail, Message
#from email.MIMEText import MIMEText
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from flask.ext.sendmail import Message
import re
import smtplib
import os

import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# index view function suppressed for brevity
app = Flask(__name__)

#app.secret_key = 'development key'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


@app.route('/',methods=['GET', 'POST'])
@app.route('/index')
def index():
    #form = ContactForm()
    #print("Your in the contact section")
    quotes = quote()
    return render_template("index.html",quote=quotes[0],author=quotes[1])



@app.route('/result',methods = ['POST', 'GET'])
def result():
   mail = Mail(app)
   form = ContactForm()

   if request.method == 'POST':
        result = request.form
        for k,v in result.items():
            print(k,v)
            if k == "contactEmail":
                #print("contact email")
                if valid_email(v.strip()) == False:
                    flash('Email is not correct')
                    return redirect(url_for('index',_anchor='contact'))
            #check if string is empty
            if not v.strip():
                flash('All fields are required.')
                print("flash")
                return redirect(url_for('index',_anchor='contact'))
        print("Your message has been sent")


        #MAIL_SERVER = 'smtp.googlemail.com'
        #MAIL_PORT = 465
        #MAIL_USE_TLS = False
        #MAIL_USE_SSL = True
        #MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')



    #    msg = Message(recipients=result["contactEmail"],
        #            sender="powerm3@tcd.ie",
        #              body=result["contactMessage"],
        #              subject=result["contactSubject"])

        #mail.send(msg)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = result["contactSubject"]
        msg['From'] = result["contactName"]
        msg['To'] = "Michael Power"

        msg.attach(MIMEText(result["contactMessage"], 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_USERNAME, [result["contactEmail"].strip(),"powerm3@tcd.ie"], msg.as_string())
        server.close()


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


def quote():
# Set the URL you want to webscrape from
    url = 'https://www.brainyquote.com/quote_of_the_dayl'

# Connect to the URL
    response = requests.get(url)

# Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")

#print(soup)

#quote is in meta tag
    quote = soup.findAll('meta')

#print(quote)

#find the twtter description as the quote lies in that reference
    for i in quote:
        try:
            if(i.attrs['name']=='twitter:description'):
            #print(i.attrs['content'])
                quote_of_the_day = i.attrs['content']
        except:
            a = 1

#remove quotes
    newstr = quote_of_the_day.replace('"', "")

#split string into quote and author
    spit = newstr.split('-')
    return spit



if __name__ == '__main__':
    app.run()

#Build a scrapper for the quotes section of the site to change it everyday
