from flask import Flask, render_template, request, redirect, url_for, make_response
from model import User, db
import hashlib, uuid

app = Flask(__name__)
db.create_all() #Erstellt neue datenbank tabellen

@app.route("/")
def index():
    session_token = request.cookies.get("session_token")
    if session_token:
     user = db.query(User).filter_by(session_token=session_token).first()
    else:
        user = None
    return render_template("index.html", user=user)
@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    password=request.form.get("user-password")
    hashpas=hashlib.sha256(password.encode()).hexdigest()
    #neues objekt vom Typ User (Model)
    #user = User.fetch_one(query=["email", "==", email])
    user = db.query(User).filter_by(email=email).first()
    if not user:
         user = User(name=name, email=email, password=hashpas)
         db.add(user)
         db.commit()
    if hashpas != user.password:
        return  "Worng Paswword! Try again!"
    elif hashpas == user.password:
        session_token = str(uuid.uuid4())
        user.session_token = session_token
        db.add(user)
        db.commit()
        #Cookie
        response = make_response(redirect(url_for('index')))
        response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')
        return response
if __name__ == '__main__':
    app.run()