#JRN18 Due 9/29  The program in this file is the individual work of Justin Nahorny
from flask import Flask, render_template, request
from datetime import datetime
from pathlib import Path
import sqlite3 as sql
app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/enternew')
def write_recipe():
	return render_template('addRecipe.html')
	
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
	
	

	


@app.route('/list')
def list():
	con = sql.connect("recipebase.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	
	cur.execute("SELECT * FROM recipe ORDER BY Name DESC ")
	
	rows = cur.fetchall()
	return render_template("list.html",rows = rows)



@app.route('/addrec',methods = ['POST','GET'])
def addrec():
	if request.method == 'POST':
		try:

			name = request.form['Recipe']
			ingredients = request.form['Ingredients']
			steps = request.form['Steps']
			print ("id: ",id_assign,"name: ",name,"steps: ",steps,"ingredients: ",ingredients,"\n")

			with sql.connect("recipebase.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO Recipe (RecipeID,Name,Steps,Ingredients) VALUES (?,?,?,?)", (id_assign,name, steps, ingredients))
				con.commit()
				
				msg = "Recipe Successfully added"

		except:
			con.rollback()
			msg = "error in insert operations"
			
		finally:
			return render_template("result.html",msg = msg)
			con.close()


if __name__ == '__main__':
   app.run(host='0.0.0.0');
   id_assign=1
