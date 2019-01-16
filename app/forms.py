from flask_wtf import Form
from wtforms import StringField, BooleanField,TextField, TextAreaField, SubmitField,validators
from wtforms.validators import DataRequired, ValidationError


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class ContactForm(Form):
  name = TextField("Name", [validators.Required("Please enter your name.")] )
  email = TextField("Email",[validators.Required("Please enter your email address")] )
  subject = TextField("Subject",[validators.Required("Please enter the subject")])
  message = TextAreaField("Message",[validators.Required("Please enter a message")])
  submit = SubmitField("Send")
