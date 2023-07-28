# External Imports
from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from flask_login import login_required

# Internal Imports
from map_inventory.helpers import token_required
from map_inventory.models import db, MapMarkers, map_marker_schema, map_markers_schema
from map_inventory.forms import MapForm

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some': 'value'}

# Create Marker Endpoint
@api.route('/markers', methods = ['POST'])
@token_required
def create_marker(my_user):
    store_name = request.json['store_name']
    address = request.json['address']
    user_token = my_user.token

    print(f"User Token: {my_user.token}")

    marker = MapMarkers(store_name, address, user_token)

    db.session.add(marker)
    db.session.commit()

    response = map_marker_schema.dump(marker)

    return jsonify(response)

# Read 1 Marker Endpoint
@api.route('markers/<id>', methods = ['GET'])
@token_required
def get_marker(my_user, id):
    if id:
        marker = MapMarkers.query.get(id)
        response = map_marker_schema.dump(marker)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401
    
# Read all the markers
@api.route('/markers', methods = ['GET'])
@token_required
def get_markers(my_user):
    token = my_user.token
    markers = MapMarkers.query.filter_by(user_token = token).all()
    response = map_markers_schema.dump(markers)

    return jsonify(response)

# Update 1 Marker by ID
@api.get('/markers/update')
@login_required
def update_marker():

    args = dict(request.args)
    
    marker = MapMarkers.query.get(args['marker_id'])
    marker.store_name = args['store_name']
    marker.address = args['address']

    db.session.commit()

    # response = map_marker_schema.dump(marker)

    # return jsonify(response)

    return redirect(url_for('site.profile'))

# Delete 1 marker by ID
@api.route('/markers/<id>/delete')
@login_required
def delete_marker(id):
    
    marker = MapMarkers.query.get(id)

    db.session.delete(marker)
    db.session.commit()

    response = map_marker_schema.dump(marker)

    return redirect(url_for('site.profile'))

    # return jsonify(response)
