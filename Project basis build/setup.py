



import sqlite3

conn = sqlite3.connect('recipebase.db')
print("Opened database successfully")

conn.execute('CREATE TABLE Recipe (RecipeID INTEGER, Name TEXT, Steps Text, Ingredients TEXT)')
print ("Reviews table created successfully")
#Recipes have a unique ID which can be used to match to Steps and Ingredients. 
#They will have a name and once we rework the HTML we should remove steps and ingredients and instead connect to their given tables based off RID (Recipe ID)

conn.execute('CREATE TABLE Pantry (UserID INTEGER, Name TEXT, Type TEXT, Quantity INTEGER, Measurement TEXT)')
print("Pantry table created successfully")
#Pantry connects based off a unique UID (User ID) and presents a name of ingredient, the type of ingredient (Fruit, vegetable, meat), quantity present and the measurement used for the quantity

conn.execute('CREATE TABLE Steps (RecipeID INTEGER, StepValue INTEGER, Step TEXT, StepAmount INTEGER)')
print("Steps Table created successfully")
#Steps connects to a given recipe based off the RID, it tracks the text of any given step, the value of the step (step 1 --> step 2 --> step 3) 
#and a max stepamount so the system knows how many steps to read for for a given RID

conn.execute('CREATE TABLE Ingredients (RecipeID INTEGER, IngredientValue INTEGER, Ingredient TEXT, Measurement TEXT, Quantity INTEGER, IngredientAmount INTEGER)')
print("Ingredients Table created successfully")
#ingredients connects to a given recipe based off the RID, Saves an ingredient value to organize the list, (ing 1 ing 2 ing 3), 
#the name of the ingredient, the quantity being measured and the quantity present, we should also track the number of ingredients for any given RID

# conn.execute('CREATE TABLE Ingredients ()') # Commented for now, not used in implementation 1


# print ("Ratings Table created Successfully") # Commented for now, not used in implementation 1

conn.close()
