import imp
import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy import exists

from forms import RegisterForm, LoginForm, ReviewForm
from models import db, connect_db, User, Anime, Reviews
from secret import secret_key

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///capstone"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = secret_key
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

db.create_all()


@app.route("/")
def homepage():
    """Homepage of site; redirect to register."""

    return redirect("/login")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if "username" in session:
        return redirect(f"/user")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        

        user = User.register(username, password)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/user")

    else:
        return render_template("users/register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    if "username" in session:
        return redirect("/user")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            session['username'] = user.username
            return redirect("/user")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/login")

@app.route("/user")
def userPage():
  """Go to users page"""
  if "username" in session:
    reviews = Reviews.query.filter_by(user=session['username'])
    return render_template("/userpage.html", reviews=reviews)
  else:
    flash("You are not logged in. Please login to see your page.")
    return redirect("/login")


@app.route("/animeList", methods=['GET', 'POST'])
def animeList():

  """Go to anime search page"""
  if request.method == "POST":
    animeName = request.form.getlist("animeName")
    animeId = request.form.getlist("animeId")
    anime = Anime(name = animeName[0], anime_DB_id = animeId[0])
    
    if "username" in session:
        exists = db.session.query(db.exists().where(Anime.name == animeName[0]))
    
        if exists:
            flash("You have already viewed this anime!")
            return redirect("/user")
        
        db.session.add(anime)
        db.session.commit()
        return redirect(url_for("reviews", animeName= animeName[0]))


    else:   
        flash("You are not logged in. Please login to review an anime.")
        return redirect("/login")
    
   
  return render_template("/animeList.html")


@app.route("/review/<animeName>", methods=["GET", "POST"])
def reviews(animeName):
  """Go to review page"""
  form = ReviewForm()
  if form.validate_on_submit():
    rating = form.rating.data
    comments = form.comments.data

    review = Reviews(user=session['username'], anime_id=animeName, rating=rating, comments=comments)
    db.session.add(review)
    db.session.commit()

    return redirect("/user")
  return render_template("/reviews.html", animeName=animeName, form=form)

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
