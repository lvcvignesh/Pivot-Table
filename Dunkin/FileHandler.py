"""

Python module that takes care of reading from files and returning appropriate values

"""
import os
import os.path
import json
from itertools import islice
from datetime import date

SEPERATOR = '/'
BASE_PATH = 'Data'+SEPERATOR
NIFTYLIST = {'ind_niftylist.csv' : 'CNX50',
			 'ind_nifty500list.csv': 'CNX500'		
			}
class StockFile:


	def __init__(self,stock,extension):
		
		self.stock = stock
		self.extension = extension
		self.index = self.stock.index
		
	def read_from_file(self,dir_name,start, number_of_lines):
		filename = BASE_PATH+self.index+SEPERATOR+dir_name+SEPERATOR+self.stock.name+'.'+self.extension
		#print start, number_of_lines
		if(os.path.isfile(filename)):
			with open(filename) as myfile:
				"+ 1 is done because of 1st line in file " 
				head = list(islice(myfile, start, number_of_lines))
				return head
		else :
			mydate = date.today()
			try:
				self.stock.save_historical_data('1-1-1976',mydate.strftime('%d-%m-%Y'),'m')
			except:
				print self.stock.name
				raise ValueError
			return self.read_from_file(dir_name,start,number_of_lines) 
	#def
	def write_to_file(self,mode,dir_name,data):
		filename = BASE_PATH+self.index+SEPERATOR+dir_name+SEPERATOR+self.stock.name+'.'+self.extension
		directory = os.path.dirname(filename) 
		if not os.path.exists(directory):
  		  os.makedirs(directory)
  		with open(filename, mode) as f:
			f.write(data)

	def write_dict_to_file(self,dir_name,data,mode,name = None):
		if name is None:
			name = self.stock.stock
		extension = 'txt'
		filename = BASE_PATH+self.index+SEPERATOR+dir_name+SEPERATOR+name+'.'+extension
		directory = os.path.dirname(filename) 
		if not os.path.exists(directory):
  		  os.makedirs(directory)
  		with open(filename, mode) as outfile:
			json.dump(data, outfile)

	def read_dict_from_file(self,dir_name,name = None):
		extension = 'txt'
		if name is None:
			name = self.stock.stock
		filename = BASE_PATH+self.index+SEPERATOR+dir_name+SEPERATOR+name+'.'+extension
		if(os.path.isfile(filename)):
			with open(filename) as myfile:
				"+ 1 is done because of 1st line in file " 
				data = json.load(myfile)
			return data
		
	def read_monthly_data(self,start,number_of_lines):
		dir_name= 'Monthly'
		self.read_from_file(dir_name,number_of_lines)
	
	def read_daily_data(self,number_of_lines):
		dir_name= 'Daily'
		self.read_from_file(dir_name,number_of_lines)
	
	def write_monthly_data(self,mode,data):
		dir_name = 'Monthly'
		self.write_to_file(mode,dir_name,data)

	def write_daily_data(self,mode,data):
		dir_name = 'Daily'
		self.write_to_file(mode,dir_name,data)

	def write_hlc(self,data,mode):
		dir_name = 'HLC'
		self.write_dict_to_file(dir_name,data,mode)	

	def write_content(self,data,mode):
		dir_name = 'Daily'
		name ='Stocks Content'
		self.write_dict_to_file(dir_name,data,mode,name)
	
	def read_hlc(self):
		dir_name = 'HLC'
		return self.read_dict_from_file(dir_name)

	def read_content(self):
		dir_name = 'Daily'
		name ='Stocks Content'
		return self.read_dict_from_file(dir_name,name)
	#def change_extension(self,new_extension)