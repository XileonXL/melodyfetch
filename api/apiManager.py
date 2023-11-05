# -*- coding: utf-8 -*-
import json
from json import JSONEncoder, JSONDecoder
from datetime import date, datetime

from bson.objectid import ObjectId

class ApiManager(object):
	@staticmethod
	def encodeResponse(response):
		return json.dumps(response, cls = DateTimeEncoder, ensure_ascii = False).encode('utf-8')
	
	@staticmethod
	def decodeResponse(response):
		return json.loads(response, cls = DateTimeDecoder)

##############################################################################################
## 		UTILS
##############################################################################################

class DateTimeDecoder(json.JSONDecoder):
	def __init__(self, *args, **kargs):
		JSONDecoder.__init__(self, object_hook=self.dict_to_object,
							 *args, **kargs)
	
	def dict_to_object(self, d): 
		if '__type__' not in d:
			return d

		type = d.pop('__type__')
		try:
			if type == 'date':
				dateobj = date(**d)
			elif type == 'datetime':
				dateobj = datetime(**d)
			return dateobj
		except:
			d['__type__'] = type
			return d

class DateTimeEncoder(JSONEncoder):
	""" Instead of letting the default encoder convert datetime to string,
		convert datetime objects into a dict, which can be decoded by the
		DateTimeDecoder
	"""
		
	def default(self, obj):
		if isinstance(obj, datetime):
			return {
				'__type__' : 'datetime',
				'year' : obj.year,
				'month' : obj.month,
				'day' : obj.day,
				'hour' : obj.hour,
				'minute' : obj.minute,
				'second' : obj.second,
				'microsecond' : obj.microsecond,
			} 
		elif isinstance(obj, date):
			return {
				'__type__' : 'date',
				'year' : obj.year,
				'month' : obj.month,
				'day' : obj.day,
			} 
		elif isinstance(obj, ObjectId): 
			return str(obj)
		else:
			return JSONEncoder.default(self, obj)
