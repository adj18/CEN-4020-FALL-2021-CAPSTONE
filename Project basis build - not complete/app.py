
from flask import Flask, render_template, request
from datetime import datetime
from pathlib import Path
import sqlite3 as sql
app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/enternew')
def write_review():
	return render_template('addRecipe.html')
	
@app.route("/getRecipe")
def getreview():
	return render_template('getRecipe.html')
	
@app.route('/getrec',methods = ['POST','GET'])
def getrev():
	if request.method == 'POST':
		try:
			flag = 0
			#resturant = request.form['resturant']
			#print("\n\nrest =",rest,"\n\n")
			with sql.connect("recipebase.db") as con:
				con.row_factory = sql.Row
				cur = con.cursor()
			
				#cur.execute('select Reviews.Username, Reviews.Review, Reviews.Rating from Reviews where Reviews.Resturant = ?',[rest])
				
				
				rows = cur.fetchall()
		except:
			msg = "No results found"
			flag = 1
			
		finally:
		    	if flag == 0:
		    		#return render_template("showReviews.html",rows = rows)
		    	else: 
		    		return render_template("result.html",msg = msg)	
		    	con.close()
	
	

	


@app.route('/list')
def list():
	con = sql.connect("recipebase.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	
	#cur.execute("SELECT * FROM Ratings ORDER BY Resturant DESC")
	
	rows = cur.fetchall()
	return render_template("list.html",rows = rows)



@app.route('/addrec',methods = ['POST','GET'])
def addrev():
	if request.method == 'POST':
		try:
		
			#nm = request.form['username']
			#rest = request.form['resturant']
			#fd = request.form['food']
			#srvc = request.form['service']
			#ambnc = request.form['ambience']
			#pc = request.form['price']
			#rvw = request.form['Review']
			#ovrll = (float(fd)+float(srvc)+float(ambnc)+float(pc) )/ 4
			#print("\n\nnm = ", nm, "rest =",rest,"fd =", fd,"srvc =",srvc, "ambnc =",ambnc,"pc =",pc,"rvw = ",rvw, "ovrll = ",ovrll,"\n\n")
			#print (Path('reviewData.db').absolute())
			#now = datetime.now()
			#dt = now.strftime("%m-%d-%Y %H:%M:%S")
			#print ("date = ",dt,"\n\n")
			with sql.connect("reviewData.db") as con:
				cur = con.cursor()
				#cur.execute("INSERT INTO Reviews (Username,Resturant,ReviewTime,Rating,Review) VALUES (?,?,?,?,?)",(nm,rest,dt,ovrll,rvw))
				#cur.execute("INSERT INTO Ratings (Resturant, Food, Service, Ambience, Price, Overall) VALUES (?, ?, ?, ?, ?, ?)",(rest,float(fd),float(srvc),float(ambnc),float(pc),ovrll))
				
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
