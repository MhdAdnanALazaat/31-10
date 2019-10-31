from flask import Flask, render_template, request, redirect, url_for, make_response
from model import User, db
app = Flask(__name__)
db.create_all() #Erstellt neue datenbank tabellen

@app.route("/")
def index():
    email_address = request.cookies.get("email")
    if email_address:
     user = db.query(User).filter_by(email=email_address).first()
    else:
        user = None
    return render_template("index.html", user=user)
@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    #neues objekt vom Typ User (Model)
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    #Cookie
    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", email)
    return response
if __name__ == '__main__':
    app.run()