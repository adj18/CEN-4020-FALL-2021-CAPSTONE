In order to compile you will need to first create a python virtual enviornment. 

python3 -m venv /target/folder 

this can be done in a separate folder if desired.
Once created you will need to activate the virtual enviornment, to do so may vary depending on the shell currently in use. 
	ie for bash it will be: 
		source bin/activate

now you must change your directory to be inside the project directory. 
you may need to install sqlite3 (varies depending on OS)

finally you must install flask.
	pip install flask
you need to be on the newest version of pip. (system will notify you if you require an update)