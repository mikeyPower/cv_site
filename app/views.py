from flask import render_template, flash, redirect, request, Flask, url_for
from forms import ContactForm

from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import smtplib
import os
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import MySQLdb
import datetime


# index view function suppressed for brevity
app = Flask(__name__)

#app.secret_key = 'development key'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ['DB_HOST']
DB_USERNAME = os.environ['DB_USERNAME']
DB_NAME = os.environ['DB_NAME']




@app.route('/',methods=['GET', 'POST'])
def index():

    date = getTodaysDate()
    quotes = quote()
    cursor = connection()
    cur = cursor[0]
    db = cursor[1]
    todays_date = datetime.datetime.now()
    today = todays_date.strftime('%Y-%m-%d')
    try:
        cur.execute("INSERT INTO quotes(quote,quote_date,author) VALUES (%s, %s, %s)", (quotes[0], today, quotes[1]))
        db.commit()
    except:
        print()
    return render_template("index.html",quote=quotes[0],author=quotes[1],day=date)


#mail server
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
            if not v.strip() and k != "contactSubject":
                flash('Fields marked with a * should not be empty')
                print("flash")
                return redirect(url_for('index',_anchor='contact'))
        print("Your message has been sent")



        msg = MIMEMultipart('alternative')
        msg['Subject'] = result["contactSubject"]
        msg['From'] = result["contactName"]
        msg['To'] = "Michael Power"

        msg.attach(MIMEText("Thank you for visiting www.mickpowers.com\n"+"This is a recipt of your"+
       " message please do not reply to this email\n" + "Kind Regards,\n" + "Michael Power\n" +
       "=================================================================================================\n"+
       result["contactMessage"], 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_USERNAME, [result["contactEmail"].strip(),"powerm3@tcd.ie"],
       msg.as_string())

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


#web scrapper to get quotes everyday
def quote():
# Set the URL you want to webscrape from
    url = 'https://www.brainyquote.com/quote_of_the_day'

# Connect to the URL
    response = requests.get(url)

# Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")

#print(soup)

#quote is in meta tag
    quote = soup.findAll('meta')
    quote_of_the_day = ""


#find the twtter description as the quote lies in that reference
    for i in quote:
        try:
            if(i.attrs['name']=='twitter:description'):
            #print(i.attrs['content'])
                quote_of_the_day = i.attrs['content']
        except:
            a = "Not everything that is faced can be changed, but nothing can be changed until it is faced.-James Baldwin"


        #check if quote of the day string is empty
    if not quote_of_the_day:
        quote_of_the_day = a

#remove quotes
    newstr = quote_of_the_day.replace('"', "")

#split string into quote and author
    spit = newstr.rsplit('-',1)
    return spit



def getTodaysDate():
    day_endings = {
    1: 'st',
    2: 'nd',
    3: 'rd',
    21: 'st',
    22: 'nd',
    23: 'rd',
    31: 'st'}
    now = datetime.datetime.now()
    suffix = int(now.strftime("%d"))
    return(now.strftime("%B %d")+day_endings.get(suffix, 'th'))


# Start MySQL database connection returning connection state and database
def connection():
    dbconn = MySQLdb.connect(host = DB_HOST,
                             user = DB_USERNAME,
                             passwd = DB_PASSWORD,
                             db = DB_NAME)
    cur = dbconn.cursor()
    return (cur, dbconn)


if __name__ == '__main__':
    app.run()

