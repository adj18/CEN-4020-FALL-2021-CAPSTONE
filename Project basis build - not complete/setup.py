



import sqlite3

conn = sqlite3.connect('recipebase.db')
print("Opened database successfully")

conn.execute('CREATE TABLE Recipe (RecipeID INTEGER, Name TEXT, Steps Text, Ingredients TEXT)')
print ("Reviews table created successfully")


# conn.execute('CREATE TABLE Ingredients ()') # Commented for now, not used in implementation 1


# print ("Ratings Table created Successfully") # Commented for now, not used in implementation 1

conn.close()
