import lib.Config as Config
import bcrypt
import MySQLdb
import getpass

createTable = """
  DROP TABLE IF EXISTS `users`;

  CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,\
  `user` varchar(128) NOT NULL,
  `pass` varchar(128) NOT NULL,
  `email` varchar(128) NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;
"""

config = Config().getConfig()
db = MySQLdb.connect(
	host=config['mysql']['host'],
	port=config['mysql']['port'],
	user=config['mysql']['user'],
	passwd=config['mysql']['pass'],
	db=config['mysql']['db']
	)
db.autocommit(True)
cursor = db.cursor()

user = raw_input("Username: ")
email= raw_input("Email: ")
passw= getpass.getpass("Password: ")
passc= getpass.getpass("Confirm password: ")
if passw != passc:
	print("Passwords do not match!")
	exit

print("Creating database")
q = cursor.execute(createTable);
cursor.close()

print("Encrypting password")
password = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt(10))

userData = (user, password, email)
cursor = db.cursor()
q = cursor.execute("INSERT INTO users (`user`,`pass`,`email`) VALUES (%s,%s,%s)",userData)

print("Done! You can now log in with user: "+user)