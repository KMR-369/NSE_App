from flask import Flask,Blueprint,render_template,url_for,redirect,flash,session,request
from google.cloud import bigquery
import os
from datetime import date,timedelta

second = Blueprint("second",__name__,static_folder="static",template_folder="templates")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/Users/MA20422878/Python/NSE_App/dark-subject-406012-5d602fd1d71b.json'
client = bigquery.Client.from_service_account_json(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

# second = Blueprint("second",__name__,static_folder="static",template_folder="templates")
# credentials = service_account.Credentials.from_service_account_file('/Users/MA20422878/Python/NSE_App/suswa-bigquery-b56bf1bc90d0.json',scopes=['https://www.googleapis.com/auth/cloud-platform'],)

query_date = "SELECT DISTINCT DATE FROM `dark-subject-406012.nse_data.nse_data_table` ORDER BY DATE DESC"
load_dates = client.query(query_date).result().to_dataframe()
dates = []
for i in load_dates.index:
    dates.append(load_dates['DATE'][i])

def query(date):

    str1 = "SELECT * FROM `dark-subject-406012.nse_data.nse_data_table` WHERE DATE = "
    str2 = "date({},{},{}) ORDER BY SECURITY".format(int(date[0:4]),int(date[5:7]),int(date[8:]))

    query_string = str1+str2
    query_job = client.query(query_string).result().to_dataframe()

    return query_job

@second.route("/user", methods = ["POST","GET"])
def user():
    if "email" and "fname" in session:
        if request.method == "POST":
            date=request.form['selectedDate']
            return render_template("data.html",values=query(date),values1=dates)
        else:
            return render_template("data.html",values=query(str(load_dates['DATE'][0])),values1=dates)
    else:
        flash("Please login to your Account")
        return redirect(url_for("login"))