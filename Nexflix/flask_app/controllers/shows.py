from flask_app.models.user import User
from flask_app.models.show import Show

from flask_app import app
from flask import Flask, request, redirect, render_template, session, flash


# displays the new show form
@app.route("/shows/new")
def New_show():
    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")
    return render_template("new_show.html")


@app.post("/shows/create")
def create_show():
    # This route processes the new record for
    if "user_id" not in session:
        flash(
            "please login.",
        )
        return redirect("/")

    if not Show.shows_validate(request.form):
        return redirect("/shows/new")
    # The following method of writing the dictionary makes sure it retrieves all the data within the dictionary
    show_data = {
        **request.form,
        "user_id": session["user_id"],
    }
    # under here the form is valid!!

    # checking if the show already exists
    if Show.count_by_title(request.form["title"]) >= 1:
        flash("That show already exists.")
        return redirect("/shows/new")

    if "comments" in session:
        session.pop("comments")
    Show.add_show(show_data)
    return redirect("/shows/all")


@app.route("/shows/all")
def all_shows():
    """This route renders all the shows"""
    print("gggggggggggg")
    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    # Retrieve all shows
    user_show = Show.find_all_with_users()
    # Retrieve user
    user = User.find_by_user_id(session["user_id"])
    # Process shows data if needed

    # Pass processed shows to the template
    return render_template("shows.html", user=user, user_show=user_show)


@app.route("/shows/<int:show_id>")
def one_show(show_id):
    """This route displays one show"""
    one_show = Show.find_one_with_user(show_id)
    return render_template("one_show.html", one_show=one_show)


@app.route("/shows/edit/<int:show_id>")
def edit(show_id):
    user = User.find_by_user_id(session["user_id"])
    edit_show = Show.find_one_with_user(show_id)
    return render_template("edit.html", user=user, edit_show=edit_show)


@app.route("/shows/update", methods=["POST"])
def update():
    print("shows update funcdkjsfhasdjdnasldsalkd")
    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    Show.update(request.form)
    return redirect("/shows/all")


@app.route("/shows/delete/<int:show_id>")
def delete(show_id):
    Show.delete(show_id)
    return redirect("/shows/all")
