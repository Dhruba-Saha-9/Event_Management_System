from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, DateField, SelectField, TextAreaField, TimeField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from datetime import date

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    email = StringField('Email Address', validators=[
        DataRequired(),
        Email(message='Please enter a valid email address')
    ])
    phone = StringField('Phone Number (Optional)', validators=[
        Optional(),
        Length(max=20, message='Phone number must be less than 20 characters')
    ])
    submit = SubmitField('Register for Event')

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[
        DataRequired(),
        Length(min=3, max=150, message='Title must be between 3 and 150 characters')
    ])
    description = TextAreaField('Event Description (Optional)', validators=[
        Optional(),
        Length(max=500, message='Description must be less than 500 characters')
    ])
    date = DateField('Event Date', validators=[
        DataRequired()
    ])
    time = TimeField('Event Time (Optional)', validators=[
        Optional()
    ])
    hall = SelectField('Venue', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Create Event')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    submit = SubmitField('Sign In')

class HallForm(FlaskForm):
    name = StringField('Hall Name', validators=[
        DataRequired(),
        Length(min=2, max=100, message='Hall name must be between 2 and 100 characters')
    ])
    capacity = IntegerField('Capacity', validators=[
        DataRequired(),
        NumberRange(min=1, max=10000, message='Capacity must be between 1 and 10,000')
    ])
    latitude = StringField('Latitude (Optional)', validators=[
        Optional(),
        Length(max=20, message='Latitude must be less than 20 characters')
    ])
    longitude = StringField('Longitude (Optional)', validators=[
        Optional(),
        Length(max=20, message='Longitude must be less than 20 characters')
    ])
    submit = SubmitField('Add Venue')
