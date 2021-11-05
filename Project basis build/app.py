
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
	return render_template('addPantry.html')
	
@app.route("/getRecipe")
def getrecipe():
	return render_template('getRecipe.html')


@app.route('/getrec',methods = ['POST','GET'])
def getrec():
	if request.method == 'POST':
		try:
			flag = 0
			name = request.form['Recipe']

			with sql.connect("recipebase.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()

				cur.execute('SELECT Recipe.Name, Recipe.Ingredients,Recipe.Steps FROM Recipe where Recipe.Name = ? ',[name])				
				rows = cur.fetchall()
		except:
			msg = "No results found"
			flag = 1
			
		finally:
		    	if flag == 0:
		    		return render_template("showRecipes.html",rows = rows)
		    	else: 
		    		return render_template("result.html",msg = msg)	
		    	con.close()
	
	


@app.route('/listpant')
def listpant():
	con = sql.connect("recipebase.db")
	con.row_factory = sql.Row		
	cur = con.cursor()

	cur.execute("SELECT Pantry.Name, Pantry.Quantity, Pantry.Measurement FROM Pantry ORDER BY Pantry.Name DESC ")

	rows = cur.fetchall()
	return render_template('listpant.html', rows = rows)


@app.route('/list')
def list():
	con = sql.connect("recipebase.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	
	cur.execute("SELECT Recipe.Name FROM Recipe;")
	#cur.execute("SELECT Name FROM Recipe ")
	rows = cur.fetchall()
	print(rows)
	return render_template("list.html",rows = rows)




@app.route('/addrec',methods = ['POST','GET'])
def addrec():
	flag = 0
	if request.method == 'POST':
		try:
			
			name = request.form['Recipe']
			ingredients = request.form['Ingredients']
			steps = request.form['Steps']			

		

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
						cur.execute("INSERT INTO Steps (RecipeID,StepValue,Step) VALUES (?,?,?)",(id,step_counter,current_step))
							
					for char in ingredients:
						if char != '\n':
							current_ingredient += char 
						else:
							ingredient_counter +=1
							numofingredients +=1
							cur.execute("INSERT INTO Ingredients (RecipeID,IngredientValue,Ingredient) VALUES (?,?,?)",(id,ingredient_counter,current_ingredient))
							print("inserted into Ingredients")
							current_ingredient = ""
						cur.execute("INSERT INTO Ingredients (RecipeID,IngredientValue,Ingredient) VALUES (?,?,?)",(id,ingredient_counter,current_ingredient))
					
					cur.execute("INSERT INTO Recipe (RecipeID,Name,NumSteps,NumIngredients) VALUES (?,?,?,?)", (id,name, numofsteps, ingredients))
					print("inserted into Recipe")
					# cur.execute("INSERT INTO Steps (RecipeID,StepValue,Step,StepAmount) VALUES (?,?,?,?)", (1,name, numofsteps, steps,1))
					con.commit()	
					msg = "Recipe Successfully added"
				else:
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
	print("attempting to add ingredient")
	if request.method == 'POST':
		try:
			Name = request.form['Name']
			Quantity = request.form['Quantity']
			Measurement = request.form['Measurement']
			print ("UserID: ",1,"Name: ",Name,"Quantity: ",Quantity,"Measurement: ",Measurement,"\n")

			with sql.connect("recipebase.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO Pantry (UserID,Name,Quantity,Measurement) VALUES (?,?,?,?)", (1,Name, Quantity, Measurement))
				con.commit()
				
				msg = "Ingredient Successfully added to Pantry"

		except:
			con.rollback()
			msg = "error in insert operations"

		finally:
			return render_template('result.html',msg = msg)
			con.close()
	

 



if __name__ == '__main__':
   app.run(host='0.0.0.0');

