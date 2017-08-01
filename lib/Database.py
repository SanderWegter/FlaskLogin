import lib.Config as Config
import MySQLdb

class Database:
	conn = None

	def connect(self):
		config = Config().getConfig()
		
		self.conn = MySQLdb.connect(
			host=config['mysql']['host'],
			port=config['mysql']['port'],
			user=config['mysql']['user'],
			passwd=config['mysql']['pass'],
			db=config['mysql']['db']
			)
		self.conn.autocommit(True)
		self.conn.set_character_set('utf8')

	def query(self, sql, args=None):
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql,args)
		except:
			self.connect()
			cursor = self.conn.cursor()
			cursor.execute(sql,args)
		return cursor