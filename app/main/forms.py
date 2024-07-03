from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from  wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from ..models import User
from flask_login import current_user



class WriteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    story = StringField('Write a story',validators=[DataRequired()])
    submit = SubmitField('Publish')


class EditProfile(FlaskForm):
    user = StringField('Username')
    bio = TextAreaField('Add more about you')
    picture_upload = FileField('Upload profile picture', validators = [FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')


    def username(self, field):
       
        if field.data != current_user.user :
           user = User.query.filter_by(username = field.data).all()
           if user:
            raise ValidationError('Username exists. Please choose another username')