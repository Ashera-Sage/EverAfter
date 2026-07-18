from flask import Flask,render_template,request,redirect,url_for,session,flash

app=Flask(__name__)
app.secret_key="everafter_secret_key"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin_login.html")

@app.route("/admin_login",methods=["POST"])
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

if __name__=="__main__":
    app.run(debug=True)