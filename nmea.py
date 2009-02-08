import plistlib
import os


def verify(line):
	if line[0] == '$' and len(line) <= 82:
		checksum = 0
		for i in range(1, len(line)):
			if line[i] != '*':
				checksum ^= ord(line[i])
			
			else:
				try:
					if checksum == int(line[i + 1:], 16):
						return True
				
				except:
					break
	
	return False

def split(line):
	if verify(line):
		return line[1:].replace('*', ',').split(',')
	
	return None



class NMEA:
	def __init__(self, **kwargs):
		self.__hash = {}
		self.__path	= '...'
		
		self.__queue = []
		
		self.__handlers = {}
		
		if 'tmap' in kwargs:
			self.load_tmap(kwargs.get('tmap'))
	
	def __repr__(self):
		return '<NMEA(tmap=%s)>' % self.__path
	
	
	def load_tmap(self, path):
		self.__hash.clear()
		self.__path = '...'
		
		if not os.path.exists(path) and os.path.exists(os.path.join(os.path.dirname(__file__), path)):
			path = os.path.join(os.path.dirname(__file__), path)
		
		try:
			self.__hash = plistlib.readPlist(path)
			self.__path	= path
		
		except:
			pass
	
	
	def valid_keys(self):
		return self.__hash.keys()
	
	
	def unpack(self, sentence):
		data = split(sentence)
		
		if data[0] in self.__hash:
			keys = {}
			for item in self.__hash[data[0]].keys():
				index = self.__hash[data[0]][item]
				if type(index) == int:
					keys[item] = data[1:][index]
				
				else:
					keys[item] = []
					for x, y in list((index,)):
						keys[item] += data[1:][x:y]
			
			return data[0], keys
		
		return None, None
	
	
	def push(self, sentence):
		self.__queue += [sentence.strip()]
	
	
	def push_handlers(self, **kwargs):
		for talker, function in kwargs.items():
			if talker not in self.__handlers:
				self.__handlers[talker] = []
			
			self.__handlers[talker] += [function]
	
	
	def pump_messages(self):
		for sentence in self.__queue:
			talker, data = self.unpack(sentence)
			
			if 'raw' in self.__handlers:
				for handler in self.__handlers['raw']:
					handler(sentence)
			
			if 'all' in self.__handlers:
				for handler in self.__handlers['all']:
					handler(talker, data)
			
			if talker in self.__handlers:
				for handler in self.__handlers[talker]:
					handler(data)
		
		self.__queue[:] = []
	
