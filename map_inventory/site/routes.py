# External Imports
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

# Internal Imports
from map_inventory.forms import MapForm
from map_inventory.models import MapMarkers, db


site = Blueprint("site", __name__, template_folder="site_templates")

@site.route("/")
def home():
    return render_template("landing.html")

@site.route("/contact")
def contact():
    return render_template("contact.html")

@site.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    mapform = MapForm()

    try:
        if request.method == 'POST' and mapform.validate_on_submit():
            store_name = mapform.store_name.data
            address = mapform.address.data
            user_token = current_user.token

            marker = MapMarkers(store_name, address, user_token)

            db.session.add(marker)
            db.session.commit()

            return redirect(url_for('site.profile'))
        
    except:
        raise Exception('Marker not created, please check your form and try again.')
    
    user_token = current_user.token
    markers = MapMarkers.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=mapform, markers=markers)