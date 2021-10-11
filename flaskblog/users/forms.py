from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user

class RegisterationForm(FlaskForm):
    username = StringField(label='Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(label='Email', 
                           validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', 
                           validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', 
                           validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label="Sign Up")
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already taken choose another")
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("This email is already taken choose another")    

class LoginForm(FlaskForm):
    email = StringField(label='Email', 
                           validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', 
                           validators=[DataRequired()])
    remember = BooleanField(label="Remember Me")
    submit = SubmitField(label="Login")
    
class UpdateAccountForm(FlaskForm):
    username = StringField(label='Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(label='Email', 
                           validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField(label="Update Values")
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username is already taken choose another")
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("This email is already taken choose another")  