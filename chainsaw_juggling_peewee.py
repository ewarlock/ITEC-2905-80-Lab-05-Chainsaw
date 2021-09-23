"""
Build a Python application which stores the following example data in a SQLite database. Use the sqlite3 library, and write SQL statements.

    Your program should let the user add a new row for a record holder.
    Your program should also let the user search for a record holder, by name
    You should be able to update the number of catches for a record holder.  
    And, you should be able to delete a record, by record holder's name (for example, if a person's record was found to be invalid).
"""

"""
Chainsaw Juggling Record Holders as of July 2018
Name 	        Country 	Number of catches
Janne Mustonen 	Finland 	98
Ian Stewart 	Canada 	    94
Aaron Gregg 	Canada 	    88
Chad Taylor 	USA 	    78

"""

from peewee import *

db = SqliteDatabase('peewee_chainsaw.sqlite')

class Juggler(Model): 

    name = CharField()
    # username = CharField(unique=True) to make it unique
    country = CharField()
    catches = IntegerField()

    class Meta: 
        database = db
    
    def __str__(self):
        return f'{self.id}.  {self.name}, {self.country}, {self.catches}'

def create_table():
    # I realized that my program works without the db.connect() and db.close() in each function ?
    # it was interfering with testing was getting the same error about the connection already being open
    # until I removed those from the function and now am able to both run and test program... ???
    db.connect()
    db.create_tables([Juggler]) # expects a list of tables

    db.close()
    
def display_all_jugglers():

    jugglers = Juggler.select() 
    juggler_list = []
    for juggler in jugglers:
        juggler_list.append(juggler)

    return juggler_list

def search_for_juggler(search_term):

    search_result = Juggler.select().where(Juggler.name.contains(search_term))
    result_list = []
    for result in search_result:
        result_list.append(result)
        
    return result_list

def add_juggler(name, country, catches):

    juggler = Juggler.get_or_none(name=name)

    if juggler == None:
        juggler = Juggler(name=name, country=country, catches=catches)
        juggler.save()
    else:
        print(f'Juggler with name {name} already exists in database. Please use unique name.')


    
def edit_juggler(name, catches):

    rows_mod = Juggler.update(catches=catches).where(Juggler.name == name).execute()

    if rows_mod == 0:
        print(f'No juggler found with the name {name}.')
    else:
        print(f'Juggler with name {name} has been updated.')
    

    

def delete_juggler(name):

    rows_mod = Juggler.delete().where(Juggler.name == name).execute()

    if rows_mod == 0:
        print(f'No juggler found with the name {name}.')
    else:
        print(f'Juggler with name {name} has been deleted.')
 




def main():

    create_table()

    menu_text = """
    1. Display all records
    2. Add new record
    3. Edit existing record
    4. Delete record 
    5. Search by name
    6. Quit
    """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            jugglers = display_all_jugglers()
            print(jugglers)
        elif choice == '2':
            name = input('Type in juggler name: ')
            country = input('Type in juggler\'s country: ')
            catches = input('Type in number of catches: ')

            add_juggler(name, country, catches)
        elif choice == '3':
            name = input('Enter the name of the juggler to edit: ')
            catches = input(f'Enter the updated number of catches for {name}: ')

            edit_juggler(name, catches)
        elif choice == '4':
            name = input('Enter the name of the juggler to delete: ')

            delete_juggler(name)
        elif choice == '5':
            name = input('Type in all or part of juggler name: ')

            search_result = search_for_juggler(name)
            print('The following jugglers were found: ')
            print(search_result)
        elif choice == '6':
            break
        else:
            print('Not a valid selection, please try again')



if __name__ == '__main__':
    main()