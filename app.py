from flask import Flask, render_template, redirect, request, jsonify, session, url_for
# import lib.Config as Config
# import lib.Database as Database
# import lib.Users as Users

from lib.Config import Config
from lib.Database import Database
from lib.Users import Users

app = Flask(__name__)

# Initial configuration
if __name__ == "__main__":
	config = Config().getConfig()	
	app.secret_key = config['server']['appKey']

# Routes 
@app.route("/")
def index():
	if 'username' not in session:
		return redirect(url_for('login'))
	return render_template("index.html", title="Main page")

@app.route("/login", methods=['GET', 'POST'])
def login():
	error = request.args.get('error') or None
	if 'username' in session:
		return redirect(url_for('index'))

	if request.method == 'POST':
		user = request.form['username']
		passw= request.form['password']
		loginResult = Users().login(user,passw)
		if loginResult['result'] == "Failed":
			return redirect(url_for('login', error=loginResult['reason']))
		return redirect(url_for('index'))
	return render_template('login.html', title="Login", error=error)

@app.route("/logout")
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

# Run application
if __name__ == "__main__":
	options = {
		"host": config['server']['ip'],
		"port": config['server']['port'],
		"debug": config['server']['debug']
	}

	if config['ssl']['enabled']:
		options.update({"ssl_context": (config['ssl']['cert'],config['ssl']['cert'])})

	app.run(**options)