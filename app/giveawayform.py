from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, BooleanField, SelectField, TextAreaField, validators

types = ['Shoes', 'Watch', 'Hangbag', 'Clothes']

class GiveAwayForm(FlaskForm):
	photo = FileField(validators=[FileRequired()])
	gatype = SelectField("gatype", choices=[(f, f) for f in types])
	gatitle = StringField("gatitle", [validators.Length(min=4, max=25)])
	description = TextAreaField("description")


