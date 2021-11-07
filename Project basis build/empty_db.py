import sqlite3

conn = sqlite3.connect('recipebase.db')
print("Opened database successfully")

conn.execute("DROP Table Recipe")
print("Removed Recipe Table")

conn.execute("DROP Table Pantry")
print("Removed Pantry Table")

conn.execute("DROP Table Steps")
print("Removed Steps Table")


conn.execute("DROP Table Ingredients")
print("Removed Ingredients Table")

conn.close()