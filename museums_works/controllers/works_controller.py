from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.museum import Museum
from models.work import Work
import repositories.museum_repository as museum_repository
import repositories.work_repository as work_repository

works_blueprint = Blueprint("works", __name__)

# INDEX
# GET '/works'
@works_blueprint.route("/works")
def works():
    works = work_repository.select_all() #the way to access the DB is via the work_respository
    return render_template("works/index.html", all_works = works)


# NEW
# GET '/works/new'
# GET a form to fill
# NEW (NEW and CREATE are combined, because we need to create but we also need to post it back to the DB
# this is the first step. See CREATE for the second step)
@works_blueprint.route("/works/new", methods={'GET'})
def new_work():
    museums = museum_repository.select_all()
    return render_template("/works/new.html", all_museums=museums)


# CREATE
# POST '/works'
# post the form to fill the database
@works_blueprint.route("/works", methods=['POST'])
def create_work():
    title = request.form['title']
    artist = request.form['artist']
    year = request.form['year']
    museum_id = request.form['museum_id']
    
    museum = museum_repository.select(museum_id) # this line is accessing the DB to find the exact museum, by using the id number. The Museum variable needs to be defined first, before the python object is created. 
    work = Work(title, artist, year, museum) #this line is creating the object in PYTHON NOT SQL!!!
    work_repository.save(work)
    return redirect('/works')





# SHOW
# GET '/works/<id>'

# EDIT
# GET '/works/<id>/edit'

# UPDATE
# PUT '/works/<id>'



# DELETE
# DELETE '/works/<id>'
@works_blueprint.route("/works/<id>/delete", methods=['POST'])
def delete_work(id):
    work_repository.delete(id)
    return redirect('/works')

