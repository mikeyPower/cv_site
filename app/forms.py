from flask_wtf import Form
from wtforms import StringField, BooleanField,TextField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class ContactForm(Form):
  name = TextField("Name", )
  email = TextField("Email" )
  subject = TextField("Subject")
  message = TextAreaField("Message")
  submit = SubmitField("Send")
