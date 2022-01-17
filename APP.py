from turtle import heading
from flask import Flask, g, request, render_template, redirect, session, url_for
import requests
from json import loads as deserialize

app = Flask(__name__, static_url_path='')
app.secret_key = "thisisasecretkey"
url = "http://192.168.1.26:5001"

headings = ("ID", "First_Name", "Last_Name", "Time_In", "Date_In")
@app.route("/")
def LoginPage():
    if "public_id" in session:
        public_id = session["public_id"]
        return redirect("/homepage")
    else:
        return render_template("login.html")

@app.route("/", methods = ["GET","POST"])
def user_login():
    if request.method =="POST":
        reqEmailLog = request.form['email']
        reqPassLog = request.form['password']
        user_CRED = {
                'email':reqEmailLog,
                'password':reqPassLog,
                }
        json_data = requests.post(url + '/api/login', json = user_CRED, verify=False)
        des_cont = deserialize(json_data.content)
        session["public_id"]= (des_cont["public_id"])
        return redirect("/homepage")

@app.route("/register", methods = ["GET", "POST"])
def user_register():
    if "public_id" in session:
        return redirect("/homepage")
    else:
        if request.method == "POST":
            regEmail = request.form['email']
            regPass = request.form['password']
            reqFname = request.form['fname']
            reqLname = request.form['lname']
            reqMobile_Number = request.form['mobile_number']
            user_CRED = {
                'email':regEmail,
                'password':regPass,
                'fname':reqFname,
                'lname':reqLname,
                'mobile_number':reqMobile_Number
                }
            requests.post(url + '/api/registerAdmin', json = user_CRED, verify=False)
            return redirect("/")
        return render_template("register.html")

@app.route("/homepage", methods = ["GET", "POST"])
def homepage():
    if "public_id" in session:
        return render_template("homepage.html")
    else:
        return redirect("/")

@app.route("/admin", methods = ["GET", "POST"])
def admin():
    if "public_id" in session:
        return render_template("admin.html")
    else:
        return redirect("/")

@app.route("/visitor", methods = ["GET", "POST"])
def visitor():
    if "public_id" in session:
        return render_template("homepage.html")
    else:
        return redirect("/")

@app.route("/team", methods = ["GET", "POST"])
def team():
    if "public_id" in session:
        return render_template("team.html")
    else:
        return redirect("/")
    
@app.route("/registerVisitor", methods = ["GET", "POST"])
def registerVisitor():
    if request.method == "POST":
            regEmail = request.form['email']
            regPass = request.form['password']
            reqFname = request.form['fname']
            reqLname = request.form['lname']
            reqMobile_Number = request.form['mobile_number']
            user_CRED = {
                'email':regEmail,
                'password':regPass,
                'fname':reqFname,
                'lname':reqLname,
                'mobile_number':reqMobile_Number
                }
            requests.post(url + '/api/registerVisitor', json = user_CRED, verify=False)
            return redirect("http://qrcodescan.in")
    return render_template("visitorRegister.html")

@app.route("/TrafalgarPass", methods = ["GET","POST"])
def visitorLogin():
    if request.method =="POST":
        reqEmailLog = request.form['email']
        reqPassLog = request.form['password']
        user_CRED = {
                'email':reqEmailLog,
                'password':reqPassLog,
                }
        json_data = requests.post(url + '/api/visitorLogin', json = user_CRED, verify=False)
        des_cont = deserialize(json_data.content)
        session["public_id"]= (des_cont["public_id"])
        return redirect("/success")
    return render_template("TrafalgarPass.html")

@app.route("/success")
def success():
    return render_template("message.html")

@app.route("/logout")
def logout():
    session.pop("public_id", None)
    return redirect("/")

if __name__== "__main__":
    app.run(host="0.0.0.0", debug=True)