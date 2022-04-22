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



#didnt need this - included it by accident!
# SHOW
# GET '/museums/<id>'
@museums_blueprint.route("/museums/<id>", methods=['GET'])
def show_museum(id):
    museum = museum_repository.select(id)
    return render_template("museums/show.html", museum = museum)




# EDIT (EDIT and UPDATE are combined)
# Step 1:
# GET '/museums/<id>/edit'
@museums_blueprint.route("/museums/<id>/edit", methods=["GET"])
def edit_museum(id):
    museum = museum_repository.select(id) #singular museum, becasue we only want to identify ONE museum to edit, by its id number
    return render_template("museums/edit.html", museum = museum)



# UPDATE
# PUT '/museums/<id>'
@museums_blueprint.route("/museums/<id>", methods=['POST'])
def update_museum(id):
    name = request.form['name']
    address = request.form['address']
    
    museum = Museum(name, address, id) 
    museum_repository.update(museum)
    return redirect('/museums')




# DELETE
# DELETE '/museums/<id>'
@museums_blueprint.route("/museums/<id>/delete", methods=['POST'])
def delete_museum(id):
    museum_repository.delete(id)
    return redirect('/museums')
