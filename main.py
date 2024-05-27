from flask import Flask,render_template,url_for,request,redirect,session,flash
# from flask_sqlalchemy import SQLAlchemy
from google.cloud import bigquery
import os

from second import second

app = Flask(__name__)
app.register_blueprint(second,url_prefix="")
app.secret_key = "hello"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/Users/MA20422878/Python/NSE_App/dark-subject-406012-5d602fd1d71b.json'

client = bigquery.Client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

""" db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer, primary_key= True)
    first_name = db.Column("fname", db.String(100))
    last_name = db.Column("lname",db.String(100))
    mobile = db.Column("mob",db.String(20))
    email = db.Column("email",db.String(100))
    password = db.Column("password",db.String(100))

    def __init__(self,first_name,last_name,mobile,email,password):
        self.first_name= first_name
        self.last_name= last_name
        self.mobile= mobile
        self.email= email
        self.password= password
"""
@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods = ["POST","GET"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        query_string = "SELECT * FROM `dark-subject-406012.nse_data.user_data` WHERE email = '{}' ".format(email)

        find_user = client.query(query_string).result().to_dataframe()

        if not find_user.empty and find_user['email'][0] == email and find_user['password'][0] == password:
            session["email"] = find_user['email'][0]
            session["fname"] = find_user['password'][0]
            return redirect(url_for("second.user"))
        else:
            flash("Invalid Credentials")
        
        return render_template("login.html")
    else:

        return render_template("login.html")

@app.route("/signup" , methods = ["POST","GET"])
def signup():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        mobile = request.form["mob"]
        email = request.form["email"]
        password = request.form["password"]

        table_ref = client.dataset('nse_data').table('user_data')
        table = client.get_table(table_ref)
        rows_to_insert = [(fname,lname,mobile,email,password)]
        errors = client.insert_rows(table, rows_to_insert) 
        print(errors)

        """ usr = users(fname,lname,mobile,email,password)
        db.create_all()
        db.session.add(usr)
        db.session.commit() """
        flash("Registration Succesful,Login to your Account")
        return redirect(url_for("login"))
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    user = session["fname"]
    flash(f"You are succesfully logged out!, {user}")
    session.pop("fname",None)
    session.pop("email",None)
    return redirect(url_for("login"))

@app.route("/graph")
def graph():
    return render_template("graph.html")

if(__name__ == "__main__"):
    app.run()