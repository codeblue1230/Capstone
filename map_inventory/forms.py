# External Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserSignUpForm(FlaskForm):
    firstname = StringField("First Name", validators = [DataRequired()])
    lastname = StringField("Last Name", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired(), Email()])
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit_button = SubmitField("Sign Up")

class UserLoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit_button = SubmitField("Sign In")

class MapForm(FlaskForm):
    store_name = StringField('Store Name')
    address = StringField('Address')
    submit_button = SubmitField("Submit")