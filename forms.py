from wtforms.validators import DataRequired, Length, Email
from wtforms.fields import StringField, SubmitField
from flask_wtf import FlaskForm


class ResumeForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired(), Length(min=4, max=20)])
    address = StringField("Address", validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone number", validators=[DataRequired()])
    jobs = StringField("Your jobs", validators=[DataRequired()])
    skills = StringField("Your skills", validators=[DataRequired()])
    education = StringField("Education", validators=[DataRequired()])
    experience = StringField("Experience", validators=[DataRequired()])

    submit = SubmitField("Make a resume")

