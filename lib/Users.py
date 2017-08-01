import lib.Config as Config
import lib.Database as Database
import bcrypt
from flask import session

class Users:
	def __init__(self):
		self.db = Database()
	
	def login(self, username, password):
		try:
			cur = self.db.query("SELECT COUNT(1),pass FROM users WHERE user = %s", [username])
			result = cur.fetchone()
			if result[0] == 0:
				return {"result": "Failed", "reason": "User does not exist"}
			passwd = result[1]
			if bcrypt.hashpw(password.encode('utf-8'), passwd) == passwd:
				session['username'] = username
				return {"result": "Success", "reason": ""}
			return {"result": "Failed", "reason": "Wrong password"}
		except:
			return {"result": "Failed", "reason": "Database error"}

	def register(self, username, password, email):
		try:
			if not username or not password or not email:
				return {"result": "Failed", "reason": "Please fill in all fields"}
			password = bcrypt.hashpw(password.encode('utf-8'), brcrypt.gensalt(10))

			cur = self.db.query("SELECT COUNT(*) FROM users WHERE user = %s", [username])
			if (cur.fetchone()[0] > 0):
				return {"result": "Failed", "reason": "User exists"}

			cur = self.db.query("INSERT INTO users (`user`,`email`,`pass`) VALUES (%s,%s,%s)",[username, email, password])
			return {"result": "Success", "reason": ""}
		except:
			return {"result": "Failed", "reason": "Database error"}