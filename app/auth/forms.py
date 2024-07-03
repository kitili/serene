from flask_wtf import FlaskForm
from wtforms  import StringField, PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length,Email,EqualTo, ValidationError
from app import db, login_manager
from ..models import User

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Enter your email',validators=[DataRequired(), Email()])
    password = PasswordField('password',validators=[DataRequired(),Length(min=6),EqualTo('confirm_password', message = 'passwords must match')])
    confirm_password = PasswordField('Confirm password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("Username already exist. Please choose another one")


    def validate_email(self,email):
      user = User.query.filter_by(email = email.data).first()
      if user:
          raise ValidationError("Email already exists")




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
    Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')



