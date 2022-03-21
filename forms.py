from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

class Prefered(FlaskForm):
	arguments = StringField("Arguments")
	attacks = StringField("Attacks")
	semantics = SelectField("Semantics", choices = ["grounded", "preferred", "stable", "semistable"])
	prefered = SubmitField("Submit")