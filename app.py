from multiprocessing.heap import reduce_arena
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, redirect, render_template, request, flash
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

app.config['SECRET_KEY'] = "Cats_are_cool!"
debug = DebugToolbarExtension(app)


@app.route("/")
def show_homepage():
    """Shows the home page"""
    pets = Pet.query.all()
    return render_template("home.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Pet add form; handle adding."""

    form = AddPetForm()
    """GET request shows form to add a new pet.
    POST request submits new pet and commits to db"""
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        pet = Pet(**data)
        db.session.add(pet)
        db.session.commit()
        flash(f"{pet.species}, {pet.name} added!")
        return redirect("/")
    else:
        return render_template(
            "add_pet_form.html", form=form)

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def show_pet(pet_id):
    """GET request shows details for pet and form to update details.
    POST request submits updates to pet details"""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.add(pet)
        db.session.commit()
        flash(f"Details for {pet.name} updated!")
        return redirect("/")
    else:
        return render_template("pet-details.html", pet=pet, form=form)
