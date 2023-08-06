import datetime
import time
	
class Screenwriter:

	prefix_pattern = ''

	def __init__(self, p_prefix_pattern='%Y-%m-%d %H:%M:%S '):
		self.prefix_pattern = p_prefix_pattern

	def echo (self, mesg=''):
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime(self.prefix_pattern)
		print (str(st) + str(mesg))
