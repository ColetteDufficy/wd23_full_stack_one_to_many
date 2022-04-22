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



#SELECT_BY_ID
def select(id):
    work = None
    sql = """
        SELECT * FROM works 
        WHERE id = %s
    """ 
    values = [id] 
    result = run_sql(sql, values)[0]
    
    if result is not None:
        museum = museum_repository.select(result['museum_id']) #this is the museum_repo method of 'select' rather than the works_repo method of 'select'. there are a lot of dupliacte of function names in these files, so we must be clear which method we want to.
        work = Work(
            result['title'], 
            result['artist'], 
            result['year'], 
            museum, 
            result['id'] )
    return work



#DELETE ALL
def delete_all():
    sql = "DELETE FROM works" 
    run_sql(sql)
    
    
#DELETE_BY_ID
def delete(id):
    sql = """
        DELETE FROM works 
        WHERE id = %s
    """ 
    values = [id]
    run_sql(sql, values)
    
    

#UPDATE 
def update(work):
    sql = """
        UPDATE works 
        SET (title, artist, year, museum_id) = (%s, %s, %s, %s) 
        WHERE id = %s
    """
    values = [
        work.title, 
        work.artist, 
        work.year, 
        work.museum.id, 
        work.id
        ]
    run_sql(sql, values) 