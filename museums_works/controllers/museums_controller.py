from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.museum import Museum
import repositories.museum_repository as museum_repository

museums_blueprint = Blueprint("museums", __name__)

# INDEX
# GET '/museums'
@museums_blueprint.route("/museums")
def museums():
    museums = museum_repository.select_all() #the way to access the DB is via the museum_repository
    return render_template("museums/index.html", all_museums = museums)


# NEW (NEW and CREATE are combined, because we need to create but we alos need to post it back to the DB
# GET '/museums/new'
# this is the first step. See CREATE for the second step)
# create a form to fill
@museums_blueprint.route("/museums/new", methods={'GET'})
def new_museum():
    museums = museum_repository.select_all()
    return render_template("/museums/new.html", all_museums = museums)



# CREATE
# POST '/museums'
# post the form to fill the database
@museums_blueprint.route("/museums", methods=['POST'])
def create_museum():
    name = request.form['name']
    address = request.form['address']
    
    museum = Museum(name, address) #this line is creating the object in python
    museum_repository.save(museum)
    return redirect('/museums')




# SHOW
# GET '/museums/<id>'

# EDIT
# GET '/museums/<id>/edit'

# UPDATE
# PUT '/museums/<id>'


# DELETE
# DELETE '/museums/<id>'
@museums_blueprint.route("/museums/<id>/delete", methods=['POST'])
def delete_museum(id):
    museum_repository.delete(id)
    return redirect('/museums')
