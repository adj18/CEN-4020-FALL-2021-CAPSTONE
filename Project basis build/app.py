
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
	return render_template('addRecipe_name.html',msg="")

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
				cur.execute("Select  IngredientValue, Ingredient, Measurement from Ingredients WHERE  Ingredients.RecipeID = ?",[id])
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

@app.route('/addrec_name',methods = ['POST','GET'])
def addrec_name():
	flag = 0
	id=1
	if request.method == 'POST':
		with sql.connect("recipebase.db") as con:
			try:
				name = request.form['Name']

				if not name:
					msg = "name cannot be blank"
					flag = -1
					return render_template("addRecipe_name.html",msg = msg)

				cur = con.cursor()
				cur.execute("Select Recipe.RecipeID from Recipe WHERE Recipe.Name = ?",[name])
				match = cur.fetchall()
				print("searching for duplicates")
				matches = []
				for m in match:
					if m:
						flag = -1
				if flag != -1:		
					cur.execute("Select Recipe.RecipeID from Recipe")
					existing = cur.fetchall()
					currentids = []
					for exist in existing:
						if exist:
							currentids.append(exist[0])
					if currentids:
						id = max(currentids)+1
					else:
						id = 1
					cur.execute("INSERT INTO Recipe (RecipeID,Name,NumSteps,NumIngredients) VALUES (?,?,?,?)", (id,name, 0, 0))
					return render_template("addRecipe_ing.html",RID=id,msg="")	
				else:
					msg = "Recipe by the same name already exists"
					flag = -1
					return render_template("addRecipe_name.html",msg = msg)
			
			except:
				msg = "An error has occurred please try again"
				return render_template("addRecipe_name.html",msg = msg)		
					

@app.route('/addrecipe_name',methods = ['POST','GET'])
def addrec():				
		return render_template("addRecipe_name.html",msg = "")

@app.route('/addrec_ing',methods = ['POST','GET'])
def addrec_ing():
	if request.method == 'POST':
		with sql.connect("recipebase.db") as con:
			cur = con.cursor()
			try:
				name = request.form['Ingredient']
				rID = request.form['RID']
				measurement = request.form['Measurement']
				quantity = request.form['Quantity']	
				Steps = request.form['Steps']

				print(f"obtained RID: {rID}, name: {name}, measurement: {measurement}, quantity: {quantity}, Steps: {Steps}")
				if not name and Steps != "2":
					msg = "error ingredient name cannot be blank"
					return render_template("addRecipe_ing.html",RID=rID,msg=msg)
				else:
				
					if Steps=="2":
						return render_template("addRecipe_Steps.html", RID=rID,msg="")

					if Steps=="1": 

						cur.execute("INSERT INTO Ingredients (RecipeID, IngredientValue, Measurement, Ingredient) VALUES (?,?,?,?)", (rID,quantity,measurement,name ))
						cur.execute("SELECT NumIngredients FROM Recipe WHERE RecipeID = ?", [rID])
						numI = cur.fetchone()
						
						cur.execute("Update Recipe SET NumIngredients = ? WHERE RecipeID = ?", [numI[0]+1,rID])
						return render_template("addRecipe_Steps.html", RID=rID,msg="")
						
					if Steps=="0":
						cur.execute("INSERT INTO Ingredients (RecipeID, IngredientValue, Measurement, Ingredient) VALUES (?,?,?,?)", (rID,quantity,measurement,name ))
						cur.execute("SELECT NumIngredients FROM Recipe WHERE RecipeID = ?", [rID])
						numI = cur.fetchone()
						cur.execute("Update Recipe SET NumIngredients = ? WHERE RecipeID = ?", [numI[0]+1,rID])
						return render_template("addRecipe_ing.html",RID=rID,msg="Ingredient Added, please enter the next ingredient")
			except:
				msg = "Sorry! An error has occurred in the submission for Recipe Ingredients. Please Try again.."
				return render_template("addRecipe_name.html",msg=msg)


@app.route('/addrec_steps',methods = ['POST','GET'])
def addrec_steps():
	if request.method == 'POST':
		with sql.connect("recipebase.db") as con:
			cur = con.cursor()
			try:
				print("attempting to get data")
				desc = request.form['Desc']
				rID = request.form['RID']
				instruction = request.form['Instr']
				Steps = request.form['Steps']

				print(f"obtained RID: {rID}")
				print(f", desc: {desc}")
				print(f", instruction: {instruction}")
				print(f" Steps: {Steps}")
				if (not desc  or not instruction )and Steps != "2":
					msg = "Description and or Instruction cannot be blank"
					return render_template("addRecipe_Steps.html",RID=rID,msg=msg)
				else:
					if Steps =="2":
						return render_template("index.html")

					if Steps=="1": 
						cur.execute("INSERT INTO Steps (RecipeID, StepValue, Step) VALUES (?,?,?)", (rID,desc, instruction))
						cur.execute("SELECT NumSteps FROM Recipe WHERE RecipeID = ?", [rID])
						numS = cur.fetchone()
						cur.execute("Update Recipe SET NumSteps = ? WHERE RecipeID = ?", [numS[0]+1,rID])
						return render_template("index.html")
						
					if Steps=="0":
						cur.execute("INSERT INTO Steps (RecipeID, StepValue, Step) VALUES (?,?,?)", (rID,desc, instruction))
						cur.execute("SELECT NumSteps FROM Recipe WHERE RecipeID = ?", [rID])
						numS = cur.fetchone()
						cur.execute("Update Recipe SET NumSteps = ? WHERE RecipeID = ?", [numS[0]+1,rID])
						return render_template("addRecipe_Steps.html",RID=rID,msg="Step Added, please enter the next step")
			except:
				msg = "Sorry! An error has occurred in the submission for Recipe Ingredients. Please Try again.."
				return render_template("addRecipe_name.html",msg=msg)
				



					
def CleanseDB():
	with sql.connect("recipebase.db") as con:
		cur = con.cursor()
		counter =0
		try:
			cur.execute("Select Recipe.RecipeID from Recipe ORDER BY Recipe.RecipeID DESC")
			Recipes = cur.fetchall()
			for recipe in Recipes:
				if recipe:
					cur.execute("Select Recipe.NumIngredients from Recipe WHERE Recipe.RecipeID = ?", [recipe[0]])
					NumI = cur.fetchall()
					cur.execute("Select Recipe.NumSteps from Recipe WHERE Recipe.RecipeID = ?", [recipe[0]])
					NumS = cur.fetchall()
					print(NumS)
					if NumI[0][0]==0 or NumS[0][0]==0:
						cur.execute("DELETE FROM Recipe WHERE RecipeID = ?", [recipe[0]])
						cur.execute("DELETE FROM Ingredients WHERE RecipeID = ?", [recipe[0]])
						cur.execute("DELETE FROM Steps WHERE RecipeID = ?", [recipe[0]])
						counter+=1
						print("deleted")
						con.commit()
			print(f"removed {counter} number of incorrect recipes ")
		except:
			print("error")
			return
			


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

   CleanseDB()
   app.run(host='0.0.0.0');
   


