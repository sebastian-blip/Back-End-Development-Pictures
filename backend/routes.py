from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        response =  jsonify(data), 200
    else:
        response =  {"message": "Internal server error"}, 500
    
    return response


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
   
    result = [item for item in data if item["id"] == id]

    if result:
        response = result[0], 200
    else:
        response = {'Error Message': 'Picture not found'}, 404
    
    return response


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():

    picture = request.json

    if not picture:
        return {"message": "Invalid input parameter"}, 422
    

    for item in data:
        if picture['id'] == item["id"]:
            return {
                "Message": f"picture with id {picture['id']} already present"
                }, 302

    try:
        data.append(picture)
    
    except NameError:
        return {"message": "data not defined"}, 500

    return picture, 201
       

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):

    picture = request.json

    if not picture:
        return {"message": "Invalid input parameter"}, 422

    for indice, item in enumerate(data):
        if id == item['id']:
            data[indice] = picture
            return picture, 200
    
    return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):

    for item in data:
        if id == item['id']:
            data.remove(item)
            return {}, 204
    
    return {"message": "picture not found"}, 404
