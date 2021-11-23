
from flask import Flask, render_template, request
from datetime import datetime
from pathlib import Path
import sqlite3 as sql
app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/addRecipe')
def write_recipe():
	return render_template('addRecipe.html')

@app.route('/addToPantry')
def write_Pantry():
	rows = getpant()
	return render_template('addPantry.html',rows = rows, msg = "")
	
@app.route("/getRecipe")
def getrecipe():
	return render_template('getRecipe.html')

@app.route("/selectRecipe",methods = ['POST','GET'])
def selectRecipe():
	flag =0
	if request.method == 'POST':
		try:
			name = request.form['Name']
			print("Recipe Name: ",name)
			with sql.connect("recipebase.db") as con:
				cur = con.cursor()
				cur.execute("Select Recipe.RecipeID from Recipe WHERE Recipe.Name = ?",[name])	
				res = cur.fetchone()	
				id = res[0]

				cur.execute("Select  StepValue, Step from Steps WHERE  Steps.RecipeID = ?",[id])	
				steps = cur.fetchall()
				cur.execute("Select  IngredientValue, Ingredient from Ingredients WHERE  Ingredients.RecipeID = ?",[id])
				ingredients = cur.fetchall()
		except:
			msg = "No results found"
			flag = 1
		finally:
			if not flag:
				msg = "found a result"
			return render_template('RecipeDetails.html',name = name,steps = steps,ingredients = ingredients)


@app.route('/getrec',methods = ['POST','GET'])
def getrec():
	if request.method == 'POST':
		try:
			flag = 0
			name = request.form['Recipe']

			with sql.connect("recipebase.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
				cur.execute("SELECT Recipe.Name FROM Recipe WHERE Recipe.Name like ?",["%"+name+"%",])
				rows = cur.fetchall()	
				print(rows)

		except:
			msg = "No results found"
			flag = 1
		finally:
			if not flag:
				msg = "found a result"
				return render_template("list.html",rows = rows,title = 'Matching Results')
			else: 
				return render_template("result.html",msg = msg)
			
	
# @app.route('/search',methods = ['POST','GET'])
# def search():
# 	if request.method == 'POST':
# 		try:
# 			flag = 0
# 			name = request.form['Recipe'] 
# 			with sql.connect("recipebase.db") as con:
# 				cur = con.cursor()
# 				cur.execute("Select Recipe.RecipeID from Recipe WHERE Recipe.Name like %?%",[name])	



# 	return render_template('')	


@app.route('/listpant')
def listpant():
	con = sql.connect("recipebase.db")
	con.row_factory = sql.Row		
	cur = con.cursor()

	cur.execute("SELECT Pantry.Name, Pantry.Quantity, Pantry.Measurement FROM Pantry ORDER BY Pantry.Name DESC ")

	rows = cur.fetchall()
	

	return render_template('listpant.html', rows = rows)



def getpant():
	con = sql.connect("recipebase.db")
	con.row_factory = sql.Row		
	cur = con.cursor()

	cur.execute("SELECT Pantry.Name, Pantry.Quantity, Pantry.Measurement FROM Pantry ORDER BY Pantry.Name DESC ")

	rows = cur.fetchall()
	

	return rows








@app.route('/list')
def list():
	con = sql.connect("recipebase.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	
	cur.execute("SELECT Recipe.Name FROM Recipe;")
	#cur.execute("SELECT Name FROM Recipe ")
	rows = cur.fetchall()
	print(rows)
	return render_template("list.html",rows = rows,title = 'Everything We\'ve Got')




@app.route('/addrec',methods = ['POST','GET'])
def addrec():
	flag = 0
	if request.method == 'POST':
		try:
			
			name = request.form['Recipe']
			ingredients = request.form['Ingredients']
			steps = request.form['Steps']			

			print(name)
			print(steps)
			print(ingredients)

			with sql.connect("recipebase.db") as con:
			
				cur = con.cursor()
				#checking for existing recipe by the same name
				cur.execute("Select Recipe.RecipeID from Recipe WHERE Recipe.Name = ?",[name])
				match = cur.fetchall()
				if not match:
					#iterate the recipe ID
					cur.execute("Select Recipe.RecipeID from Recipe ORDER BY Recipe.RecipeID DESC")
					existing = cur.fetchall()
					if not existing:
						id = 1 		
					else:
						id = existing[0][0] +1
						print("generated ID: ",id)
					#handle steps here
					current_step = ""
					current_ingredient = ""
					numofsteps = 0
					numofingredients = 0
					step_counter=0
					ingredient_counter =0
					for char in steps:
						if char != '\n':
							current_step += char 
						else:
							step_counter+=1
							numofsteps +=1
							cur.execute("INSERT INTO Steps (RecipeID,StepValue,Step) VALUES (?,?,?)",(id,step_counter,current_step))
							print("inserted into steps")
							current_step = ""
					step_counter+=1
					numofsteps +=1
					cur.execute("INSERT INTO Steps (RecipeID,StepValue,Step) VALUES (?,?,?)",(id,step_counter,current_step))
							
					for char in ingredients:
						if char != '\n' :
							current_ingredient += char 
						else:
							ingredient_counter +=1
							numofingredients +=1
							cur.execute("INSERT INTO Ingredients (RecipeID,IngredientValue,Ingredient) VALUES (?,?,?)",(id,ingredient_counter,current_ingredient))
							print("inserted into Ingredients")
							current_ingredient = ""
					ingredient_counter +=1
					numofingredients +=1
					cur.execute("INSERT INTO Ingredients (RecipeID,IngredientValue,Ingredient) VALUES (?,?,?)",(id,ingredient_counter,current_ingredient))
					
					cur.execute("INSERT INTO Recipe (RecipeID,Name,NumSteps,NumIngredients) VALUES (?,?,?,?)", (id,name, numofsteps, ingredients))
					print("inserted into Recipe, id: ",id)
					# cur.execute("INSERT INTO Steps (RecipeID,StepValue,Step,StepAmount) VALUES (?,?,?,?)", (1,name, numofsteps, steps,1))
					con.commit()	
					msg = "Recipe Successfully added"
				else:
					print("ID Select Statement: ",match)
					flag = -1
					msg = "Recipe by the same name already exists"	
				print(id)
			
		except:
			con.rollback()
			if flag == -1:
				msg = "Recipe by the same name already exists"
			else:
				msg = "error in insert operations"
			
		finally:
			return render_template("result.html",msg = msg)
			con.close()

@app.route('/addpant',methods = ['POST','GET'])
def addpant():
	flag = 0
	msg = ""
	print("attempting to add ingredient")
	if request.method == 'POST':



		with sql.connect("recipebase.db") as con:
			


				Name = request.form['Ingredient']
				Quantity = request.form['Quantity']
				Measurement = request.form['Measurement']
				print ("Name: ",Name,"Quantity: ",Quantity,"Measurement: ",Measurement,"\n")
				rows = getpant()
				
				cur = con.cursor()
				#Check if pantry element already exists
				cur.execute("Select Pantry.Name from Pantry WHERE Pantry.Name = ?",[Name])
				match = cur.fetchall()
				if not match:
					cur.execute("INSERT INTO Pantry (UserID,Name,Quantity,Measurement) VALUES (?,?,?,?)", (1,Name, Quantity, Measurement))
					con.commit()
				
					msg = "Ingredient Successfully added to Pantry"
				else:
					print("Name select statement: ",match)
					flag = -1
					msg = "Pantry item already exists"	
				return render_template('AddPantry.html',rows = rows, msg = msg)
				
	

 



if __name__ == '__main__':
   app.run(host='0.0.0.0');

