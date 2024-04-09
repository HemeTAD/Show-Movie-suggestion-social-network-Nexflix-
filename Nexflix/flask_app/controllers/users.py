from flask_app.models.user import User
from flask_app.models.show import Show

from flask_app import app, bcrypt
from flask import request, redirect, render_template, session, flash
import pprint


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/register")
def register():
    if not User.reg_validate(request.form):
        return redirect("/")
    potential_user = User.find_by_email(request.form["email"])
    if potential_user != None:
        print("user exists!!!!!!!!!!!!!!!!!!!!")
        flash("Email in use. please login.", "register")
        return redirect("/")

    # redirect to the route where the burger form is rendered.
    # else no errors:
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
    }
    # Call the save @classmethod on User
    user_id = User.register(data)
    # store user id into session
    session["user_id"] = user_id
    return redirect("/shows/all")


@app.post("/login")
def login():
    if not User.login_validate(request.form):
        return redirect("/")

    potential_user = User.find_by_email(request.form["email"])
    if potential_user == None:
        flash("Invalid credentials", "login")
        return redirect("/")

    user = potential_user
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials", "login")
        return redirect("/")

    session["user_id"] = user.id
    return redirect("/shows/all")


@app.get("/logout")
def logout():
    session.clear()
    return redirect("/")
