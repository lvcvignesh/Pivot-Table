"""

Updates all the files with recent Data

"""
from nsetools import Nse
import os
import os.path
import json
import shutil
import pprint as pprint
from itertools import islice
from datetime import date
from datetime import datetime
from pprint import pprint
from StockData import StockData
from datetime import date
from FileHandler import StockFile
EXTENSION = 'csv'
SEPERATOR = '/'
BASE_PATH = 'Data'+SEPERATOR
NIFTYLIST = {'ind_niftylist.csv' : 'CNX50',
			 'ind_nifty500list.csv': 'CNX500'		
			}
class UpdateData:

	def __init__(self,index):
		self.nse = Nse()
		self.date=date.today()
		self.index = index
		self.stock_data = {}
		self.stock_data = self.init_content()
		if self.stock_data is None:
			self.stock_data={}
			self.update_index()
		#pprint(self.stock_data)
	
	def update_index(self):
		count = 0
		with open(self.index) as myfile:
			for line in myfile:
				if count is not 0: 
					line = line.split(',')
					try:
						self.update_content(line[2])
					except:
						continue
					#self.update_hlc(line[2])
				else : 
					count = 1
		self.save_content()
	#	self.write_update('day')
	
	def get_index():
		return self.index
	def update_content(self,stock):
		try:
			print stock
			data = self.nse.get_quote(stock)
		except:
			raise ValueError
		self.stock_data[stock] = data
	
	def get_content(self,stock):
		return self.stock_data.get(stock)

	def read_dict_from_file(self,dir_name,name):
		extension = 'txt'
		index = NIFTYLIST[self.index]
		filename = BASE_PATH+index+SEPERATOR+dir_name+SEPERATOR+name+'.'+extension
		try:
			if(os.path.isfile(filename)):
				with open(filename) as myfile:
					"+ 1 is done because of 1st line in file " 
					data = json.load(myfile)
					return data
		except:
			raise ValueError
		
	
	def write_dict_to_file(self,dir_name,data,mode,name = None):
		if data is None:
			return
		extension = 'txt'
		index = NIFTYLIST[self.index]
		filename = BASE_PATH+index+SEPERATOR+dir_name+SEPERATOR+name+'.'+extension
		directory = os.path.dirname(filename) 
		if not os.path.exists(directory):
  		  os.makedirs(directory)
  		with open(filename, mode) as outfile:
			json.dump(data, outfile)

	def init_content(self):
		#self.update_index()
		name = 'Stocks Content'
		dir_name= 'Daily'
		return self.read_dict_from_file(dir_name,name)

	def save_content(self):
		name = 'Stocks Content'
		dir_name= 'Daily'
		self.write_dict_to_file(dir_name,self.stock_data,'w',name)
	
	def update_val(self,data,stock):
		change = False
		high = self.stock_data[stock]['dayHigh']
		low = self.stock_data[stock]['dayLow']
		if data['High'] < high:
			    data['High'] = high
			    change = True
		if data['Low'] > low:
			    data['Low'] = low
			    change = True
		return {"Data": data, "Change":change}
		
	def update_hlc(self,stock):
		data = self.read_dict_from_file('HLC',stock)
		change = False
		for key in data:
			val = self.update_val(data[key],stock)
			if val['Change']:
				data[key] = val['Data']
				change = True
		if change:
			self.write_dict_to_file('HLC',data,'w',stock)
			print "Updated ",stock

	def read_update(self,period):
		extension = 'txt'
		filename = BASE_PATH+'update_'+period+'.'+extension
		if(os.path.isfile(filename)):
			with open(filename) as myfile:
				head = list(islice(myfile, 1))
			return head
		else:
			self.write_update(period)
			return self.date
	
	def write_update(self,period):
		extension = 'txt'
		filename = BASE_PATH+'update_'+period+'.'+extension
		with open(filename, 'w') as outfile:
				outfile.write(self.date.strftime('%d-%m-%Y'))
	
	def update(self):
		day_update = self.read_update('day')
		month_update = self.read_update('month')
		day_update = datetime.strptime(day_update[0],'%d-%m-%Y').date()
		month_update = datetime.strptime(month_update[0],'%d-%m-%Y').date()
		flagday = False
		flagmonth =False
		count = 0
		for ind in NIFTYLIST:
			self.index = ind
			index = NIFTYLIST[ind]
			if self.date.day - day_update.day > 0 or self.date.month - day_update.month > 0:
				self.update_index()
				flagday =True
			if self.date.month - month_update.month > 0:
				if self.check_month_change(month_update.month):
					self.update_monthly()	
					shutil.rmtree(BASE_PATH+SEPERATOR+index+SEPERATOR+'HLC')
			  		flagmonth =True
			if flagday:
				self.write_update('day')
				if count ==1:
					return True
			if flagmonth:
				self.write_update('month')
				if count ==1:
					return True
			count = count + 1
		return False	

	def check_month_change(self,udate):
		data = StockData('INFY',self)
		mydate = date.today()
		#html = data.get_historical_data(mydate.strftime('%d-02-%Y'),mydate.strftime('%d-%m-%Y'),'m')
		html = data.get_today_data()
		line =html.split('\n')
		line = line[1].split(',')
		data_date = int(line[0].split('-')[1])
		val = False
		if data_date - udate > 0:
			val= True
		return val

	def update_monthly(self):
		count = 0
		with open(self.index) as myfile:
			for line in myfile:
				if count is not 0: 
					line = line.split(',')
					try:
						stock = StockData(line[2],self)
						stock.save_historical_data('1-1-1976',self.date.strftime('%d-%m-%Y'),'m')
					except:
						continue
					#self.update_hlc(line[2])
				else : 
					count = 1
		#self.write_update('month')

	def return_file_data(self):
		filename = self.index
		if(os.path.isfile(filename)):
			with open(filename) as myfile:
				"+ 1 is done because of 1st line in file " 
				head = list(islice(myfile,1,1000))
				return head

