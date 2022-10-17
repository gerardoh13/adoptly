from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange


class AddPetForm(FlaskForm):
    """Form for adding pets."""

    name = StringField("Name:", validators=[
                       InputRequired(message="Name cannot be blank")])
    species = SelectField("Species:", choices=[('cat', 'Cat'), ('dog', 'Dog'), (
        'porcupine', 'Porcupine')], validators=[InputRequired(message="Select a species")])
    photo_url = StringField("Photo URL:", validators=[
                            Optional(), URL(require_tld=True, message="Invalid URL")])
    age = IntegerField("Age:", validators=[Optional(), NumberRange(
        min=0, max=30, message="Must be between 0 and 30")])
    notes = StringField("Notes:", validators=[Optional()])

class EditPetForm(FlaskForm):
    """Form for edditing pet details."""
    photo_url = StringField("Photo URL:", validators=[
                            Optional(), URL(require_tld=True, message="Invalid URL")])
    notes = StringField("Notes:", validators=[Optional()])
    available = BooleanField("Available:")