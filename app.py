from flask import Flask, render_template, request, redirect, url_for, flash
import firebase_admin
import pyrebase
from firebase_admin import credentials, auth

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

firebase_config = {
    "databaseURL": "https://gestion-d-un-restaurant.firebaseio.com",
    "apiKey": "AIzaSyAtVwmvzlqoTCQOK9ET9aCVXm9KL5aO7_Q",
    "authDomain": "gestion-d-un-restaurant.firebaseapp.com",
    "projectId": "gestion-d-un-restaurant",
    "storageBucket": "gestion-d-un-restaurant.firebasestorage.app",
    "messagingSenderId": "816322005688",
    "appId": "1:816322005688:web:29c7f4b6a817831fc0424d",
    "measurementId": "G-N6JT97D28T"
}

firebase = pyrebase.initialize_app(firebase_config)
firebase_auth = firebase.auth()

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            firebase_auth.sign_in_with_email_and_password(email, password)
            flash("Connexion réussie !", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(str(e), "danger")
    return render_template("pages-login.html")

@app.route("/index")
def index(): 
    return render_template("index.html")

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            firebase_auth.create_user_with_email_and_password(email, password)
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(str(e), "danger")
    return render_template("pages-register.html")

@app.route("/profile_user")
def profile_user(): 
    return render_template("users-profile.html")


@app.route("/retrouver_mdp", methods=['GET', 'POST'])
def retrouver_mdp(): 
    if request.method == 'POST':
        email = request.form['email']   
        firebase_auth.send_password_reset_email(email)
        return render_template("pages-login.html")
    return render_template("retrouver-mdp.html")

@app.route("/tables_general")
def tablesGenerales(): 
    return render_template("tables-general.html")

@app.route("/tables_data")
def tablesdata(): 
    return render_template("tables-data.html")

@app.route("/pages_error")
def pages_error(): 
    return render_template("pages-error-404.html")

@app.route("/pages_contact")
def pages_contact(): 
    return render_template("pages-contact.html")

if __name__ == '__main__':
    app.run(debug=True)
