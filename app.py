from flask import Flask,render_template,request,redirect,url_for,session,flash
from datetime import datetime,date
import json

app=Flask(__name__)
app.secret_key="everafter_secret_key"

from datetime import datetime, date

@app.route("/")
def home():

    with open("data/weddings.json", "r") as file:
        weddings = json.load(file)
    upcoming = []
    completed = []
    today = date.today()
    for wedding in weddings:
        wedding_date = datetime.strptime(wedding["date"],"%Y-%m-%d").date()
        if wedding_date >= today:
            upcoming.append(wedding)
        else:
            completed.append(wedding)

    return render_template("index.html",upcoming=upcoming,completed=completed)

@app.route("/admin")
def admin():
    return render_template("admin_login.html")

@app.route("/admin-login",methods=["POST"])
def admin_login():
    username=request.form["username"]
    password=request.form["password"]
    if username=="admin" and password=="Admin@123":
        session["admin"]=True
        flash("Login Successfull","success")
        return redirect("/dashboard")
    flash("Invalid Username or Password","error")
    return redirect("/admin")

@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/admin")
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.pop("admin",None)
    flash("Logged Out Successfully","success")
    return redirect("/admin")

@app.route("/create-wedding",methods=["GET","POST"])
def create_wedding():
    if request.method=="POST":
        groom=request.form["groom"]
        bride=request.form["bride"]
        date=request.form["date"]
        time=request.form["time"]
        venue=request.form["venue"]
        place=request.form["place"]
        guests=request.form["guests"]
        description=request.form["description"]

        with open("data/weddings.json","r") as file:   # reading existing weddings
            weddings=json.load(file)

        if weddings:                                # generate id
            wedding_id=weddings[-1]["id"]+1         # last id + 1
        else:         
            wedding_id=1                            # if no items then id =1

        wedding={
            "id":wedding_id,
            "groom":groom,
            "bride":bride,
            "date":date,
            "time":time,
            "venue":venue,
            "place":place,
            "guests":int(guests),
            "description":description
        }

        weddings.append(wedding)  # adding new wedding

        with open("data/weddings.json","w") as file:  # saving to json file
            json.dump(weddings,file,indent=4)
        flash("Saved Successfully","success")
        return redirect("/dashboard")

    return render_template("create_wedding.html")

@app.route("/view-weddings")
def view_weddings():
    with open("data/weddings.json","r") as file:
        weddings=json.load(file)
    return render_template("view_weddings.html",weddings=weddings)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_wedding(id):
    with open("data/weddings.json", "r") as file:
        weddings = json.load(file)
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
        with open("data/weddings.json", "w") as file:
            json.dump(weddings, file, indent=4)
        flash("Wedding Updated Successfully!", "success")
        return redirect("/view-weddings")

    return render_template("edit.html", wedding=selected_wedding)

@app.route("/delete/<int:id>")
def delete_wedding(id):
    with open("data/weddings.json", "r") as file:
        weddings = json.load(file)
    for wedding in weddings:
        if wedding["id"] == id:
            weddings.remove(wedding)
            break
    with open("data/weddings.json", "w") as file:
        json.dump(weddings, file, indent=4)
    flash("Wedding Deleted Successfully!", "success")
    return redirect("/view-weddings")

@app.route("/invitation/<int:id>")
def invitation(id):
    with open("data/weddings.json", "r") as file:
        weddings = json.load(file)

    selected_wedding = None
    for wedding in weddings:

        if wedding["id"] == id:
            selected_wedding = wedding
            break

    return render_template("invitation.html",wedding=selected_wedding)

@app.route("/rsvp/<int:id>", methods=["GET", "POST"])
def rsvp(id):

    with open("data/weddings.json", "r") as file:
        weddings = json.load(file)

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

        with open("data/rsvps.json", "r") as file:
            rsvps = json.load(file)

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

        with open("data/rsvps.json", "w") as file:
            json.dump(rsvps, file, indent=4)

        flash("Thank you! Your RSVP has been submitted successfully.", "success")

        return redirect("/")

    return render_template("rsvp.html", wedding=selected_wedding)

@app.route("/rsvp-list")
def rsvp_list():

    with open("data/rsvps.json", "r") as file:
        rsvps = json.load(file)

    with open("data/weddings.json", "r") as file:
        weddings = json.load(file)

    for rsvp in rsvps:

        for wedding in weddings:

            if wedding["id"] == rsvp["wedding_id"]:

                rsvp["couple"] = wedding["groom"] + " ❤️ " + wedding["bride"]

                break

    return render_template("rsvp_list.html",
                           rsvps=rsvps)

if __name__=="__main__":
    app.run(debug=True)