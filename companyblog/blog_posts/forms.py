# blog_posts/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, StopValidation
from flask_wtf.file import FileRequired
from flask_wtf import Form

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    file = FileField('Upload', default='File has not been attached')
    submit = SubmitField("Post")


