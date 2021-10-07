



import sqlite3

conn = sqlite3.connect('recipebase.db')
print("Opened database successfully")

conn.execute('CREATE TABLE Recipe (RecipeID INTEGER, Name TEXT, Ingredients)')
print ("Reviews table created successfully")


conn.execute('CREATE TABLE Ingredients ()')


print ("Ratings Table created Successfully")

conn.close()
