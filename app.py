from flask import Flask,render_template,request,redirect,url_for,session,flash
import json

app=Flask(__name__)
app.secret_key="everafter_secret_key"

@app.route("/")
def home():
    return render_template("index.html")

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
        wedding={
            "groom":groom,
            "bride":bride,
            "date":date,
            "time":time,
            "venue":venue,
            "place":place,
            "guests":int(guests),
            "description":description
        }
        with open("data/weddings.json","r") as file:
            weddings=json.load(file)
            weddings.append(wedding)
        with open("data/weddings.json","w") as file:
            json.dump(weddings,file,indent=4)
        flash("Saved Successfully","success")
        return redirect("/dashboard")

    return render_template("create_wedding.html")

@app.route("/view-weddings")
def view_weddings():
    with open("data/weddings.json","r") as file:
        weddings=json.load(file)
    return render_template("view_weddings.html",weddings=weddings)

if __name__=="__main__":
    app.run(debug=True)