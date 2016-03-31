from nsetools import Nse
from pprint import pprint
import urllib2
import os
from FileHandler import StockFile
from datetime import date
from Pivot import Pivot 

BASE_URL = 'http://ichart.finance.yahoo.com/table.csv?s='
BASE_PATH = 'Data/'
NIFTYLIST = {'ind_niftylist.csv' : 'CNX50',
			 'ind_nifty500list.csv': 'CNX500'		
			}
API_KEY ='7zTazsysxctwCz4jsH8h'
MONTHLY = 'm'
DAILY = 'd'
EXTENSION = 'csv'
MODE1 ='prev'
MODE2 = 'date_diff'
class StockData:
	"""
	Class which fetches the stock data 
	Includes historical Data, end of day data 
	"""
	def __init__(self,stock,nse,sector=None):
		"""
		Checks for existance of file. If it is not present 
		fetch the historical data of the file using yahoofinance api.
		fetch current value of the stock using nsetools

		Choice file or database 
		"""
		self.stock = stock
		self.sector= sector
		self.dict = nse.get_content(stock)
		self.name = self.dict.get('companyName')
		self.index = NIFTYLIST[nse.index]
		self.file = StockFile(self,EXTENSION)
		self.date = date.today()
		self.pivot_prev = Pivot(self,MODE1)
		#self.save_content()

	def get_content(self):
		return self.dict

	def get_company_name(self):
		if self.name is None:
			self.name = self.dict.get('companyName', None)
		return self.name

	def get_close_price(self):
		return self.dict.get('closePrice', None)

	def get_last_price(self):
		return self.dict.get('lastPrice', None)
	
	def get_day_high(self):
		return self.dict.get('dayHigh', None)
	
	def get_day_low(self):
		return self.dict.get('dayLow', None)
	
	def get_previous_close(self):
		return self.dict.get('previousClose', None)

	def get_face_value(self):
		return self.dict.get('faceValue', None)

	def get_high52(self):
		return self.dict.get('high52', None)

	def get_low52(self):
		return self.dict.get('high52', None)
	
	def get_open(self):
		return self.dict.get('open', None)

	def get_quarter_number(self):
		quarter = ((self.date.month-1) / 3)+1
		return quarter  
	
	def prev_quarter_month_diff(self,extra_months = 0):
		quarter = self.get_quarter_number()
		month_diff =self.date.month - (3*(quarter-1))
		month_diff = month_diff + extra_months
		return month_diff

	def print_pivot(self):
		return {"Pivot Diff":self.pivot_diff.year_pivot,
				"Pivot Prev":self.pivot_prev.year_pivot
				}

	def get_half_year_number(self):
		half_year = ((self.date.month-1) / 6)+1
		
		return half_year
	
	def prev_half_year_month_diff(self, extra_months = 0):
		half_year = self.get_half_year_number()
		month_diff =self.date.month - (6*(half_year-1))
		return month_diff + extra_months

	def prev_year_month_diff(self,number_of_years, extra_months = 0):
		month_diff = self.date.month
		return month_diff + extra_months

	def get_today_hlc(self):
		high = self.get_day_high()
		low = self.get_day_low()
		open_price = self.get_open()
		print open_price
		close = self.get_close_price()
		if close is None:
			close = self.get_previous_close()
		return {'Open': open_price ,'High':high, 'Low':low, 'Close':close }

	#def get_week_hlc(self)

	def get_month_hlc(self,filedata):
		if filedata is not None:
			return filedata.get('Month')		
		data = self.file.read_from_file('Monthly',2,3)
		return self.get_hlc(data)

	def get_quarter_hlc(self,mode,filedata,number = 0):
		"""Read from file fetches the month Diff,
		eg :April 4th month and is in 2nd quarter so 1st month in 2nd quarter
		it returns 1 +2 is done for indexing, 3 is for quarter"""
		if filedata is not None:
			return filedata.get('Quarter')		
		if mode is MODE1:
			diff =self.prev_quarter_month_diff(number)
			diff = diff+1
			data = self.file.read_from_file('Monthly',diff,diff+3)
		else : 
			data = self.get_date_diff_quarter()
		return self.get_hlc(data)

	def get_half_year_hlc(self, mode, filedata, number=0):
		if filedata is not None:
			return filedata.get('Half Year')		
		if mode is MODE1:
			diff = self.prev_half_year_month_diff(number)
			diff = diff+1
			data = self.file.read_from_file('Monthly', diff, diff+6)
		else :
			data = self.get_date_diff_half_year()
		return self.get_hlc(data)
	
	def get_year_hlc(self, mode, filedata, number = 0):
		if filedata is not None:
			return filedata.get('Year')		
		if mode is MODE1:
			diff = self.prev_year_month_diff(1, number)
			diff = diff + 1 
			data = self.file.read_from_file('Monthly',diff,diff+12)
		else :
			data = self.get_date_diff_year()
		return self.get_hlc(data)
	
	def get_5year_hlc(self, mode,filedata , number = 0):
		if filedata is not None:
			return filedata.get('5 Years')		
		diff = self.prev_year_month_diff(5, number)	
		if mode is MODE1:
			diff = diff + 1
			data = self.file.read_from_file('Monthly', diff, diff+12*5)
		else :
			data = self.get_date_diff_5year()
		return self.get_hlc(data)

	def get_10year_hlc(self,mode,filedata, number = 0):
		if filedata is not None:
			return filedata.get('10 Years')		
		diff = self.prev_year_month_diff(10)	
		if mode is MODE1:
			data = self.file.read_from_file('Monthly',diff+1,diff+1+12*10)
		else :
			data = self.get_date_diff_10year()
		return self.get_hlc(data)

	
	def get_period_open(self,period,mode=MODE1):
		if period is 'Monthly':
			return self.get_month_hlc(self.pivot_prev.dict)['Open']
		elif period is 'Quarter':
			return self.get_quarter_hlc(mode,self.pivot_prev.dict)['Open']
		elif period is 'HalfYear':
			return self.get_half_year_hlc(mode,self.pivot_prev.dict)['Open']
		elif period is 'Year':
			return self.get_year_hlc(mode,self.pivot_prev.dict)['Open']
		elif period is 'FiveYear':
			return self.get_5year_hlc(mode,self.pivot_prev.dict)['Open']
		elif period is 'TenYear':
			return self.get_10year_hlc(mode,self.pivot_prev.dict)['Open']
		elif period is 'Today':
			return self.get_today_hlc()['Open']

	def get_multiple_quarters(self, filedata = None):
		quarter_diff = [0,3,6]
		quarter_list = []
		if filedata is not None:
			mylist =['Quarter', 'Quarter 1', 'Quarter 2']
			for months in mylist:
				print filedata.get(months) ,'multiple_quarters'
				quarter_list.append(filedata.get(months))
			if len(quarter_list) == 3:
				return quarter_list 
		for months in quarter_diff:
			quarter_list.append(self.get_quarter_hlc(MODE1,None,months))
		return quarter_list	

	def get_multiple_half_years(self, filedata = None):
		half_year_diff = [0,6,12]
		half_year_list =[]
		if filedata is not None:
			mylist =['Half Year', 'Half Year 1', 'Half Year 2']
			for months in mylist:
				half_year_list.append(filedata.get(months))
			if len(half_year_list) == 3:
				return half_year_list 
		
		for months in half_year_diff:
			half_year_list.append(self.get_half_year_hlc(MODE1,None,months))
		return half_year_list

	def get_multiple_years(self, filedata = None):
		year_diff = [0,12,24]
		year_list =[]
		if filedata is not None:
			mylist =['Year', 'Year 1', 'Year 2']
			for months in mylist:
				year_list.append(filedata.get(months))
			if len(year_list) == 3:
				return year_list 
		
		for months in year_diff:
			year_list.append(self.get_year_hlc(MODE1,None,months))
		return year_list

	def get_multiple_five_years(self, filedata = None):
		year_diff = [0,60,120]
		five_year_list = []
		if filedata is not None:
			mylist =['5 Years', '5 Years 1', '5 Years 2']
			for months in mylist:
				five_year_list.append(filedata.get(months))
			
			if len(five_year_list) == 3:
				return five_year_list 
		
		for months in year_diff:
			five_year_list.append(self.get_5year_hlc(MODE1,None,months))
		return five_year_list

	def get_multiple_ten_years(self, filedata = None):
		year_diff = [0,120,240]
		ten_year_list = []

		if filedata is not None:
			mylist =['10 Years', '10 Years 1', '10 Years 2']
			for months in mylist:
				ten_year_list.append(filedata.get(months))
			if len(ten_year_list) == 3:
				return ten_year_list 
		
		for months in year_diff:
			ten_year_list.append(self.get_10year_hlc(MODE1,None,months))
		return ten_year_list

	def get_date_diff_quarter(self):
		return self.file.read_from_file('Monthly',3)
		

	def get_date_diff_half_year(self):
		return self.file.read_from_file('Monthly',6)
		
	def get_date_diff_year(self):
		return self.file.read_from_file('Monthly',12)
		
	def get_date_diff_5year(self):
		return self.file.read_from_file('Monthly',60)
		
	def get_date_diff_10year(self):
		return self.file.read_from_file('Monthly',120)

	def get_all_pivot(self,pivot):

		data = {
				"Month" : pivot.get_month_pivot(),
				"Quarter" : pivot.get_quarter_pivot(),
				"Half Year": pivot.get_half_year_pivot(),
				"Year" : pivot.get_year_pivot(),
				"5 Years" : pivot.get_5year_pivot(),
				"10 Years" : pivot.get_10year_pivot(),
				}
		return data

	def get_hlc(self,data):
		if data is None:
			return None
		high = []
		low = []
		arr =['hello','world']
		close = self.get_close_price()
		if close is None:
			close = self.get_previous_close()
		count =0
		#print data,'yayayaya', len(data)
		for line in range(0,len(data)):
			arr = data[line].split(',')
			if count is 0:
				close = float(arr[4])
				count = 1
			high.append(float(arr[2]))
			low.append(float(arr[3]))
		open = arr[1]
		#print data
		return {'Open': open,'High':max(high), 'Low':min(low), 'Close':close}

	def get_historical_data(self,start,end,frequency):

		"Gets MAX Historical Data"
		start = start.split('-')
		end =end.split('-')
		symbol_url = '%s%s.NS&d=%s&e=%s&f=%s&g=%s&a=%s&b=%s&c=%s&ignore=.csv' % (BASE_URL, self.stock, 
			int(end[1])-1,end[0],end[2],frequency,int(start[1])-1,start[0],start[2])
		try:
			response = urllib2.urlopen(symbol_url)
			html = response.read()
		except:
			symbol_url = '%s%s.BO&d=%s&e=%s&f=%s&g=d&a=%s&b=%s&c=%s&ignore=.csv' % (BASE_URL, self.stock, 
			int(end[1])-1,end[0],end[2],int(start[1])-1,start[0],start[2])
			try:
				response = urllib2.urlopen(symbol_url)
				html = response.read()
			except:
				raise ValueError("No Data") 
		return html

	"""def write_to_file(self,data,TAG,mode):
		filename = BASE_PATH+TAG+'/'+self.stock
		directory = os.path.dirname(filename) 
		if not os.path.exists(directory):
  		  os.makedirs(directory)
  		with open(filename, mode) as f:
			f.write(data)
	"""
	def save_historical_data(self,start,end,frequency):
		#print self.name
		print self.name
		try:
			data = self.get_historical_data(start,end,frequency)
			if frequency is MONTHLY:
				self.file.write_monthly_data('w',data)
			else:
				self.file.write_daily_data('w',data)
		except:
			self.file.write_monthly_data('w',None)
			raise ValueError("No Data") 

	def get_today_data(self):
		m=int(self.date.month)-1
		d=int(self.date.day)
		flag = True
		while flag:
			try:
				symbol_url = '%s%s.NS&a=%s&b=%s&c=%s&g=m' % (BASE_URL, self.stock, 
				m,d,self.date.year)
				print symbol_url
				response = urllib2.urlopen(symbol_url)
				flag = False
			except:
				d= d-1
				continue
		html = response.read()
		return html
		

	def save_hlc(self, pivot):
		data = {
				"Month" : pivot.month_hlc,
				"Quarter" : pivot.quarter_hlc,
				"Quarter 1":pivot.multiple_quarters_hlc[1],
				"Quarter 2":pivot.multiple_quarters_hlc[2],
				"Half Year": pivot.half_year_hlc,
				"Half Year 1":pivot.multiple_half_years_hlc[1],
				"Half Year 2":pivot.multiple_half_years_hlc[2],
				"Year" : pivot.year_hlc,
				"Year 1":pivot.multiple_years_hlc[1],
				"Year 2":pivot.multiple_years_hlc[2],
				"5 Years" : pivot.five_year_hlc,
				"5 Years 1":pivot.multiple_five_years_hlc[1],
				"5 Years 2":pivot.multiple_five_years_hlc[2],
				"10 Years" : pivot.ten_year_hlc,
				"10 Years 1":pivot.multiple_ten_years_hlc[1],
				"10 Years 2":pivot.multiple_ten_years_hlc[2],
				
				}

		self.file.write_hlc(data,'w')
	
	def save_content(self):
		data = {
				self.stock : self.dict
				}
		self.file.write_content(data,'a')