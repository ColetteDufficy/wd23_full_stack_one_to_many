from db.run_sql import run_sql

from models.museum import Museum
from models.work import Work
import repositories.museum_repository as museum_repository

# Write your functions here 

#SAVE
def save(work):
    sql = """
        INSERT INTO works (title, artist, year, museum_id) 
        VALUES (%s, %s, %s, %s) 
        RETURNING *
    """
    # the term museum_id is direct from the sql file
    # no need for a semicolon at the end of the SQL statement, because psycopg2 is translating this for me
   
    values = [
        work.title, 
        work.artist, 
        work.year, 
        work.museum.id #this is the id column frm the museum table, in the work table
        ]
    results = run_sql(sql, values)
    id = results[0]['id']
    work.id = id
    return work



#SELECT_ALL
def select_all():  
    works = [] 

    sql = "SELECT * FROM works"
    results = run_sql(sql)

    for row in results:
        museum = museum_repository.select(row['museum_id'])#this extra line is needed because were trying to extract the 'id' key, from the user table, via the Task table. See line 40
        work = Work(
            row['title'], 
            row['artist'], 
            row['year'], 
            museum, 
            row['id'] 
            )
        works.append(work)
    return works 



#DELETE ALL
def delete_all():
    sql = "DELETE FROM works" 
    run_sql(sql)