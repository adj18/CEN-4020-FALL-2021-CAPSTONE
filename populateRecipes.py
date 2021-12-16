import sqlite3, json, string
with sqlite3.connect("recipebase.db") as con, open("/home/kali/Documents/CEN-4020-FALL-2021-CAPSTONE-Post-Submission/Project basis build/100recipes.json","r") as rl:
    print("Recipes database opened")
    recipes = json.load(rl)
    #recipe table schema: RecipeID, Name, NumSteps, NumIngredients 
    id=0
    Recipes = []
    for recipe in recipes["recipes"]:
            id+=1
            name = recipe['title']
            numI = 0
            numS = 0
            Ingredients = []
            steps = []
            k=0
            for ingredient in recipe['ingredients']:
                # print(ingredient)
                measurement = ""
                IName = ""
                tmpblock = ""
                frac = ""
                count = 0.0
                #get count
                tmp = ""
                tmp = ingredient.split(' ')
                if not tmp[0].isdigit(): 
                        continue

                if tmp[0].find("/") != -1:
                        frac = tmp[0].split('/')
                        count+= int(frac[0]) / int(frac[1])
                        if tmp[1] == "cups" or tmp[1] == "cup":
                                measurement = "cup"
                                for i in range(2,len(tmp)):
                                        IName+= tmp[i] 
                                        IName+=" "
                        elif tmp[1] == "teaspoons" or tmp[1] == "teaspoon":
                                measurement = "teaspoon"
                                for i in range(2,len(tmp)):
                                        IName+= tmp[i] 
                                        IName+=" "
                        elif tmp[1] == "tablespoons" or tmp[1] == "tablespoon":    
                                measurement = "tablespoon"
                                for i in range(2,len(tmp)):
                                        IName+= tmp[i] 
                                        IName+=" "
                        elif tmp[1] == "ounces" or tmp[1] == "ounce":  
                                measurement = "ounce"
                                for i in range(2,len(tmp)):
                                        IName+= tmp[i] 
                                        IName+=" "
                        elif tmp[1] == "pints" or tmp[1] == "pint": 
                                measurement = "pint"
                                for i in range(2,len(tmp)):
                                        IName+= tmp[i]  
                                        IName+=" "
                                else:
                                        measurement = "whole"
                                        for i in range(1,len(tmp)):
                                                IName+= tmp[i]  
                                                IName+=" "
                        IName = IName.lower()
                        IName = IName.capitalize()
                        Ingredients.append([id,count,measurement,IName])
                else:
                        count += int(tmp[0])
                    
                        if tmp[1].find("/") != -1:
                                frac = tmp[1].split('/')
                                count+= int(frac[0]) / int(frac[1])
                                if tmp[2] == "cups" or tmp[2] == "cup":
                                        measurement = "cup"
                                        for i in range(3,len(tmp)):
                                                IName+= tmp[i] 
                                                IName+=" "
                                elif tmp[2] == "teaspoons" or tmp[2] == "teaspoon":
                                        measurement = "teaspoon"
                                        for i in range(3,len(tmp)):
                                                IName+= tmp[i] 
                                                IName+=" "
                                elif tmp[2] == "tablespoons" or tmp[2] == "tablespoon":    
                                        measurement = "tablespoon"
                                        for i in range(3,len(tmp)):
                                                IName+= tmp[i] 
                                                IName+=" "
                                elif tmp[2] == "ounces" or tmp[2] == "ounce":  
                                        measurement = "ounce"
                                        for i in range(3,len(tmp)):
                                                IName+= tmp[i] 
                                                IName+=" "
                                elif tmp[2] == "pints" or tmp[2] == "pint": 
                                        measurement = "pint"
                                        for i in range(3,len(tmp)):
                                                IName+= tmp[i] 
                                                IName+=" " 
                                else:
                                        measurement = "whole"
                                        for i in range(2,len(tmp)):
                                                IName+= tmp[i]  
                                                IName+=" "
                        else:
                                #check for measurement if none found use whole
                                if tmp[1] == "cups" or tmp[1] == "cup":
                                        measurement = "cup"
                                        for i in range(2,len(tmp)):
                                                IName+= tmp[i] 
                                                IName+=" "
                                elif tmp[1] == "teaspoons" or tmp[1] == "teaspoon":
                                        measurement = "teaspoon"
                                        for i in range(2,len(tmp)):
                                                IName+= tmp[i] 
                                                IName+=" "
                                elif tmp[1] == "tablespoons" or tmp[1] == "tablespoon":    
                                        measurement = "tablespoon"
                                        for i in range(2,len(tmp)):
                                                IName+= tmp[i] 
                                                IName+=" "
                                elif tmp[1] == "ounces" or tmp[1] == "ounce":  
                                        measurement = "ounce"
                                        for i in range(2,len(tmp)):
                                                IName+= tmp[i] 
                                                IName+=" "
                                elif tmp[1] == "pints" or tmp[1] == "pint": 
                                        measurement = "pint"
                                        for i in range(2,len(tmp)):
                                                IName+= tmp[i] 
                                                IName+=" " 
                                else:
                                        measurement = "whole"
                                        for i in range(1,len(tmp)):
                                                IName+= tmp[i]  
                                                IName+=" "
                        IName = IName.lower()
                        IName = IName.capitalize()
                        Ingredients.append([count,measurement,IName])
            
            numI = len(Ingredients)
            for step in recipe["instructions"]:
                    split = step.split(" ")
                    desc = ""
                    for s in split[:5]:
                        desc += s
                        desc += " "
                    steps.append([desc,step])
            
            numS = len(steps)



            Recipes.append([id,name,numS,numI])
            con.execute("INSERT INTO Recipe (RecipeID, Name, NumSteps, NumIngredients) VALUES (?,?,?,?)",(id,name,numS,numI))
            for ingredient in Ingredients:
                con.execute("INSERT INTO Ingredients (RecipeID, IngredientValue, Measurement, Ingredient) VALUES (?,?,?,?)",(id,ingredient[0],ingredient[1],ingredient[2]))
            for step in steps:
                con.execute("INSERT INTO Steps (RecipeID, StepValue, Step) VALUES (?,?,?)",(id,step[0],step[1]))



