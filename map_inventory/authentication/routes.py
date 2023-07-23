# External Imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

# Internal Imports
from map_inventory.forms import UserSignUpForm, UserLoginForm
from map_inventory.models import User, db, check_password_hash

auth = Blueprint("auth", __name__, template_folder="auth_templates")

@auth.route("/signup", methods = ["GET", "POST"])
def signup():
    usersignupform = UserSignUpForm()

    try:
        if request.method == "POST" and usersignupform.validate_on_submit():
            firstname = usersignupform.firstname.data
            lastname = usersignupform.lastname.data
            email = usersignupform.email.data
            username = usersignupform.username.data
            password = usersignupform.password.data

            user = User(firstname, lastname, email, username, password)

            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a new account")

            return redirect(url_for("auth.signin"))
            
    except:
        raise Exception("Invalid Data Entered. Please Try Again")
    
    return render_template("signup.html", form=usersignupform)


@auth.route("/signin", methods = ["GET", "POST"])
def signin():
    userloginform = UserLoginForm()

    try:
        if request.method == "POST" and userloginform.validate_on_submit():
            username = userloginform.username.data
            password = userloginform.password.data

            logged_user = User.query.filter(User.username == username).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash("You have successfully logged in.")
                return redirect(url_for("site.profile"))
            else:
                flash("Your Username or Password was incorrect.")
                return redirect(url_for("auth.signin"))
            
    except:
        raise Exception("Invalid Form Data: Please Check Your Form")

    return render_template("signin.html", form=userloginform)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("site.home"))
