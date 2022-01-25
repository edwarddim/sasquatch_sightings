from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    user = User.get_one({'id' : session['user_id']})
    sightings = Sighting.get_all()
    return render_template("dashboard.html", user = user[0], sightings = sightings)

@app.route("/new/sighting")
def new_sighting():
    return render_template("new_sighting.html")

@app.route("/new/sighting", methods=["POST"])
def create_sighting():
    if 'user_id' not in session:
        return redirect("/")
    if not Sighting.validate(request.form):
        return redirect("/new/sighting")
    data = {
        **request.form,
        'user_id' : session['user_id']
    }
    Sighting.save(data)
    return redirect("/dashboard")

@app.route("/sightings/<int:sighting_id>/edit")
def edit_sighting(sighting_id):
    sighting = Sighting.get_one({"sighting_id" : sighting_id})
    print(sighting)
    return render_template('edit_sighting.html', sighting = sighting[0])

@app.route("/sightings/<int:sighting_id>/update", methods=['POST'])
def update_sightings(sighting_id):
    if not Sighting.validate(request.form):
        return redirect(f"/sightings/{sighting_id}/edit")
    Sighting.update(request.form)
    return redirect('/dashboard')

@app.route("/sightings/<int:sighting_id>/delete")
def delete_sightings(sighting_id):
    Sighting.delete({"sighting_id" : sighting_id})
    return redirect('/dashboard')

# DISPLAY ONE SIGHTING
@app.route("/sightings/<int:sighting_id>")
def show_sightings(sighting_id):
    sighting = Sighting.get_one_with_creator({"sighting_id" : sighting_id})
    skeptics = Sighting.get_skeptics({"sighting_id" : sighting_id})
    user = User.get_one({'id' : session['user_id']})

    return render_template("show_sightings.html",
        sighting = sighting,
        skeptics = skeptics,
        user = user[0]
    )



# BELIEVING AND SKEPTICAL LOGIC
@app.route("/sightings/<int:sighting_id>/believe", methods=["POST"])
def believe(sighting_id):
    data = {
        'sighting_id' : sighting_id,
        'user_id' : session['user_id']
    }
    Sighting.believe(data)
    return redirect(f"/sightings/{sighting_id}")

@app.route("/sightings/<int:sighting_id>/skeptic", methods=["POST"])
def skeptic(sighting_id):
    data = {
        'sighting_id' : sighting_id,
        'user_id' : session['user_id']
    }
    Sighting.skeptic(data)
    return redirect(f"/sightings/{sighting_id}")
