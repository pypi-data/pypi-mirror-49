import datetime
import time
	
class Screenwriter:

	prefix_pattern = ''

	def __init__(self, p_prefix_pattern='%Y-%m-%d-%H:%M:%S '):
		self.prefix_pattern = p_prefix_pattern

	def echo (self, mesg='', add_prefix=''):
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime(self.prefix_pattern)
		print (str(st) + add_prefix + str(mesg))

	def error (self, mesg=''):
		self.echo (mesg, 'ERROR: ')

	def warn (self, mesg=''):
		self.echo (mesg, 'WARN:  ')

	def info (self, mesg=''):
		self.echo (mesg, 'INFO:  ')
