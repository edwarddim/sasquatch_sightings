from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    form_data = {
        **request.form,
        'password' : pw_hash
    }
    user_id = User.save(form_data)
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route("/login", methods=['POST'])
def login():
    email = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(email)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = user_in_db.id
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    if 'warning' in session and session['warning'] == 2:
        flash("YOU WERE WARNED")
    session.clear()
    return redirect("/")