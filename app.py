from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, date
import json

app = Flask(__name__)
app.secret_key = "everafter_secret_key"                   # to keep the data stored in browser secure and safe
#---------------------------------------------------------------------------------------#
# HOME ROUTE #
@app.route("/")
def home():
    try:
        with open("data/weddings.json", "r") as file:     # to read existing file
            weddings = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):     # either if no file or if no data inside the json file then exception
        weddings = []                                     # then it takes as an empty file

    upcoming = []                                         # upcoming weddings empty
    completed = []                                        # completed weddings empty
    today = date.today()                                  # get todays date
    for wedding in weddings:                              # checking for each wedding
        wedding_date = datetime.strptime(wedding["date"],"%Y-%m-%d").date()
        # strptime = string parse time ---> to convert a string(date) to datetime object
        # we dont need time so date() used
        if wedding_date >= today:
            upcoming.append(wedding)
        else:
            completed.append(wedding)

    return render_template("index.html",upcoming=upcoming,completed=completed)
#---------------------------------------------------------------------------------------#
# ADMIN ROUTE #
@app.route("/admin")                                      # it only shows the login page
def admin():
    return render_template("admin_login.html")            # to login using username and password
#---------------------------------------------------------------------------------------#
# ADMIN LOGIN ROUTE #
@app.route("/admin-login", methods=["POST"])              # login processing happens here
def admin_login():
    username = request.form["username"]
    password = request.form["password"]
    if username == "admin" and password == "Admin@123":
        session["admin"] = True
        flash("Login Successful", "success")
        return redirect("/dashboard")                     # if true go to dashboard

    flash("Invalid Username or Password", "error")
    return redirect("/admin")                             # else stay 
#---------------------------------------------------------------------------------------#
# HOME ROUTE #
@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/admin")

    return render_template("dashboard.html")
#---------------------------------------------------------------------------------------#
# HOME ROUTE #
@app.route("/logout")
def logout():

    session.pop("admin", None)

    flash("Logged Out Successfully", "success")

    return redirect("/admin")
#---------------------------------------------------------------------------------------#
# HOME ROUTE #
@app.route("/create-wedding", methods=["GET", "POST"])
def create_wedding():

    if request.method == "POST":

        groom = request.form["groom"]
        bride = request.form["bride"]
        date = request.form["date"]
        time = request.form["time"]
        venue = request.form["venue"]
        place = request.form["place"]
        guests = request.form["guests"]
        description = request.form["description"]

        try:
            with open("data/weddings.json", "r") as file:       # reading existing weddings
                weddings = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            weddings = []

        if weddings:                     # to generate id
            wedding_id = weddings[-1]["id"] + 1            # last id + 1
        else:
            wedding_id = 1                                 # if no items then id = 1

        wedding = {
            "id": wedding_id,
            "groom": groom,
            "bride": bride,
            "date": date,
            "time": time,
            "venue": venue,
            "place": place,
            "guests": int(guests),
            "description": description
        }

        weddings.append(wedding)             # adding new wedding

        try:
            with open("data/weddings.json", "w") as file:         # saving to json file
                json.dump(weddings, file, indent=4)

            flash("Saved Successfully", "success")

        except Exception:
            flash("Error saving wedding!", "error")

        return redirect("/dashboard")

    return render_template("create_wedding.html")
#---------------------------------------------------------------------------------------#
# HOME ROUTE #
@app.route("/view-weddings")
def view_weddings():

    try:
        with open("data/weddings.json", "r") as file:
            weddings = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        weddings = []

    return render_template("view_weddings.html", weddings=weddings)
#---------------------------------------------------------------------------------------#
# HOME ROUTE #
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_wedding(id):

    try:
        with open("data/weddings.json", "r") as file:
            weddings = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        weddings = []

    selected_wedding = None

    for wedding in weddings:

        if wedding["id"] == id:

            selected_wedding = wedding

            if request.method == "POST":

                wedding["groom"] = request.form["groom"]
                wedding["bride"] = request.form["bride"]
                wedding["date"] = request.form["date"]
                wedding["time"] = request.form["time"]
                wedding["venue"] = request.form["venue"]
                wedding["place"] = request.form["place"]
                wedding["guests"] = int(request.form["guests"])
                wedding["description"] = request.form["description"]

            break

    if request.method == "POST":

        try:
            with open("data/weddings.json", "w") as file:
                json.dump(weddings, file, indent=4)

            flash("Wedding Updated Successfully!", "success")

        except Exception:
            flash("Error updating wedding!", "error")

        return redirect("/view-weddings")

    return render_template("edit.html", wedding=selected_wedding)
#---------------------------------------------------------------------------------------#
# HOME ROUTE #
@app.route("/delete/<int:id>")
def delete_wedding(id):

    try:
        with open("data/weddings.json", "r") as file:
            weddings = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        weddings = []

    for wedding in weddings:

        if wedding["id"] == id:
            weddings.remove(wedding)
            break

    try:
        with open("data/weddings.json", "w") as file:
            json.dump(weddings, file, indent=4)

        flash("Wedding Deleted Successfully!", "success")

    except Exception:
        flash("Error deleting wedding!", "error")

    return redirect("/view-weddings")
#---------------------------------------------------------------------------------------#
# HOME ROUTE #
@app.route("/invitation/<int:id>")
def invitation(id):
    try:
        with open("data/weddings.json", "r") as file:
            weddings = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        weddings = []
    selected_wedding = None
    for wedding in weddings:
        if wedding["id"] == id:
            selected_wedding = wedding
            break
    return render_template("invitation.html", wedding=selected_wedding)
#---------------------------------------------------------------------------------------#
# HOME ROUTE #
@app.route("/rsvp/<int:id>", methods=["GET", "POST"])
def rsvp(id):

    try:
        with open("data/weddings.json", "r") as file:
            weddings = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        weddings = []

    selected_wedding = None

    for wedding in weddings:

        if wedding["id"] == id:
            selected_wedding = wedding
            break

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        status = request.form["status"]
        bring_guest = request.form["bring_guest"]
        guests = int(request.form["guests"])
        message = request.form["message"]

        try:
            with open("data/rsvps.json", "r") as file:
                rsvps = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            rsvps = []

        rsvp = {

            "wedding_id": id,
            "name": name,
            "email": email,
            "phone": phone,
            "status": status,
            "bring_guest": bring_guest,
            "guests": guests,
            "message": message

        }

        rsvps.append(rsvp)

        try:
            with open("data/rsvps.json", "w") as file:
                json.dump(rsvps, file, indent=4)

            flash("Thank you! Your RSVP has been submitted successfully.", "success")

        except Exception:
            flash("Error saving RSVP!", "error")

        return redirect("/")

    return render_template("rsvp.html", wedding=selected_wedding)
#---------------------------------------------------------------------------------------#
# HOME ROUTE #
@app.route("/rsvp-list")
def rsvp_list():

    try:
        with open("data/rsvps.json", "r") as file:
            rsvps = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        rsvps = []

    try:
        with open("data/weddings.json", "r") as file:
            weddings = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        weddings = []

    for rsvp in rsvps:

        for wedding in weddings:

            if wedding["id"] == rsvp["wedding_id"]:

                rsvp["couple"] = wedding["groom"] + " ❤️ " + wedding["bride"]

                break

    return render_template("rsvp_list.html", rsvps=rsvps)
#---------------------------------------------------------------------------------------#
# HOME ROUTE #
@app.route("/summary")
def summary():

    if "admin" not in session:
        return redirect("/admin")

    try:
        with open("data/weddings.json", "r") as file:
            weddings = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        weddings = []

    try:
        with open("data/rsvps.json", "r") as file:
            rsvps = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        rsvps = []

    summary_data = []

    for wedding in weddings:

        registered = 0

        for rsvp in rsvps:

            if (rsvp["wedding_id"] == wedding["id"] and
                    rsvp["status"] == "Attending"):

                registered += int(rsvp["guests"])

        seats_left = wedding["guests"] - registered

        if seats_left > 0:
            status = "Seats Available"

        elif seats_left == 0:
            status = "Full"

        else:
            status = "Waiting List"

        summary_data.append({

            "couple": wedding["groom"] + " ❤️ " + wedding["bride"],
            "capacity": wedding["guests"],
            "registered": registered,
            "seats_left": seats_left,
            "status": status

        })

    return render_template(
        "summary.html",
        summary_data=summary_data
    )
#---------------------------------------------------------------------------------------#
if __name__ == "__main__":
    app.run(debug=True)