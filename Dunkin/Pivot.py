"""

Class to calculate the Pivot,Support and Resistance

"""
class Pivot:

	def __init__(self,stock_data,mode):

		self.stock_data = stock_data
		self.open =stock_data.get_open()
		self.dict = stock_data.file.read_dict_from_file('HLC')
		self.month_hlc = stock_data.get_month_hlc(self.dict)
		self.quarter_hlc = stock_data.get_quarter_hlc(mode,self.dict)
		self.half_year_hlc = stock_data.get_half_year_hlc(mode,self.dict)
		self.year_hlc = stock_data.get_year_hlc(mode,self.dict)
		self.five_year_hlc = stock_data.get_5year_hlc(mode,self.dict)
		self.ten_year_hlc = stock_data.get_10year_hlc(mode,self.dict)
		self.multiple_months_hlc = stock_data.get_multiple_months(self.dict)
		self.multiple_quarters_hlc = stock_data.get_multiple_quarters(self.dict)
		self.multiple_half_years_hlc = stock_data.get_multiple_half_years(self.dict)
		self.multiple_years_hlc = stock_data.get_multiple_years(self.dict)
		self.multiple_five_years_hlc = stock_data.get_multiple_five_years(self.dict)
		self.multiple_ten_years_hlc = stock_data.get_multiple_ten_years(self.dict)

		self.day_pivot = PivotData(stock_data.get_today_hlc()).calc_pivot()
		self.month_pivot = PivotData(self.month_hlc).calc_pivot()
		self.quarter_pivot = PivotData(self.quarter_hlc).calc_pivot()
		self.half_year_pivot = PivotData(self.half_year_hlc).calc_pivot()
		self.year_pivot = PivotData(self.year_hlc).calc_pivot()
		self.five_year_pivot = PivotData(self.five_year_hlc).calc_pivot()
		self.ten_year_pivot = PivotData(self.ten_year_hlc).calc_pivot()
		self.multiple_months = []
		self.multiple_quarters = []
		self.multiple_half_years = []
		self.multiple_years = []
		self.multiple_five_years = []
		self.multiple_ten_years = []

		self.get_multiple_month_hlc()
		self.get_multiple_quarter_hlc()
		self.get_multiple_half_year_hlc()
		self.get_multiple_year_hlc()
		self.get_multiple_five_year_hlc()
		self.get_multiple_ten_year_hlc()
		
		if self.dict is None:
			self.stock_data.save_hlc(self)

	"""
		Month Pivot : r1 : Resistance 1
		 			  s2 : Resistance 2
		 			  s3 : Resistance 3
					  p  : Pivot
					  s1 : Support 1
		 			  s2 : Support 2
		 			  s3 : Support 3
		 			  
	"""
	def get_month_pivot(self):
		return self.month_pivot

	def get_quarter_pivot(self):
		return self.quarter_pivot

	def get_half_year_pivot(self):
		return self.half_year_pivot

	def get_multiple_month_hlc(self):
		for hlc in self.stock_data.get_multiple_months(self.dict):
			pivot_val = PivotData(hlc).calc_pivot()
			self.multiple_months.append(pivot_val)
		if None in self.multiple_months:
			self.month_pivot['Pivot 2'] = "None"	
			self.month_pivot['Pivot 3'] = "None"
			return
		self.month_pivot['Pivot 2'] = self.multiple_months[1]["Pivot"]
		self.month_pivot['Pivot 3'] = self.multiple_months[2]["Pivot"]

	def get_multiple_quarter_hlc(self):
		for hlc in self.stock_data.get_multiple_quarters(self.dict):
			pivot_val = PivotData(hlc).calc_pivot()
			self.multiple_quarters.append(pivot_val)
		if None in self.multiple_quarters:
			self.quarter_pivot['Pivot 2'] = "None"	
			self.quarter_pivot['Pivot 3'] = "None"
			return
		self.quarter_pivot['Pivot 2'] = self.multiple_quarters[1]["Pivot"]
		self.quarter_pivot['Pivot 3'] = self.multiple_quarters[2]["Pivot"]
	
	def get_multiple_half_year_hlc(self):
		for hlc in self.stock_data.get_multiple_half_years(self.dict):
			pivot_val = PivotData(hlc).calc_pivot()
			self.multiple_half_years.append(pivot_val)
		if None in self.multiple_half_years:
			self.half_year_pivot['Pivot 2'] = "None"	
			self.half_year_pivot['Pivot 3'] = "None"
			return 
		self.half_year_pivot['Pivot 2'] = self.multiple_half_years[1]["Pivot"]
		self.half_year_pivot['Pivot 3'] = self.multiple_half_years[2]["Pivot"]
	
	def get_multiple_year_hlc(self):
		for hlc in self.stock_data.get_multiple_years(self.dict):
			pivot_val = PivotData(hlc).calc_pivot()
			self.multiple_years.append(pivot_val)
		if None in self.multiple_years:
			self.year_pivot['Pivot 2'] = "None"	
			self.year_pivot['Pivot 3'] = "None"
			return
		self.year_pivot['Pivot 2'] = self.multiple_years[1]["Pivot"]
		self.year_pivot['Pivot 3'] = self.multiple_years[2]["Pivot"]
		
	def get_multiple_five_year_hlc(self):
		for hlc in self.stock_data.get_multiple_five_years(self.dict):
			pivot_val = PivotData(hlc).calc_pivot()
			self.multiple_five_years.append(pivot_val)
		if None in self.multiple_five_years:
			self.five_year_pivot['Pivot 2'] = "None"	
			self.five_year_pivot['Pivot 3'] = "None"
			return 
		self.five_year_pivot['Pivot 2'] = self.multiple_five_years[1]["Pivot"]
		self.five_year_pivot['Pivot 3'] = self.multiple_five_years[2]["Pivot"]
	
	def get_multiple_ten_year_hlc(self):
		for hlc in self.stock_data.get_multiple_ten_years(self.dict):
			pivot_val = PivotData(hlc).calc_pivot()
			self.multiple_ten_years.append(pivot_val)
		if None in self.multiple_ten_years:
			self.ten_year_pivot['Pivot 2'] = "None"	
			self.ten_year_pivot['Pivot 3'] = "None"
			return 
		self.ten_year_pivot['Pivot 2'] = self.multiple_ten_years[1]["Pivot"]
		self.ten_year_pivot['Pivot 3'] = self.multiple_ten_years[2]["Pivot"]
	
	"""def get_multiple_year_hlc(self):
	
	def get_multiple_half_year_hlc(self):
	
	def get_multiple_year_hlc(self):
	
	def get_multiple_five_year_hlc(self):
	
	def get_multiple_ten_year_hlc(self):
	"""
	def get_year_pivot(self):
		return self.year_pivot

	def get_5year_pivot(self):
		return self.five_year_pivot

	def get_10year_pivot(self):
		return self.ten_year_pivot

	def get_pivot(self,tag):
		if tag is 'Monthly':
			return self.get_month_pivot()
		elif tag is 'Quarter':
			return self.get_quarter_pivot()
		elif tag is 'HalfYear':
			return self.get_half_year_pivot()
		elif tag is 'Year':
			return self.get_year_pivot()
		elif tag is 'FiveYear':
			return self.get_5year_pivot()
		elif tag is 'TenYear':
			return self.get_10year_pivot()
		elif tag is 'Today':
			return self.day_pivot

	def get_all_colour(self):
		return {
			'Today' : self.calc_colour(self.day_pivot),
			'Monthly' : self.calc_colour(self.month_pivot),
			'Quarter' : self.calc_colour(self.quarter_pivot),
			'HalfYear' : self.calc_colour(self.half_year_pivot),
			'Year' : self.calc_colour(self.year_pivot),
			'FiveYear' : self.calc_colour(self.five_year_pivot),
			'TenYear' : self.calc_colour(self.ten_year_pivot),
		}
	
	def calc_colour(self,pivot_dict):
		arr = ['R3','R2','R1','Pivot','S1','S2','S3']
		for i in arr:
			if self.open > pivot_dict.get(i):
				break
		if i is 'S3' and self.open < pivot_dict.get(i):
			return'S4'  
		return i


class PivotData:

	def __init__(self,hlc):
		if hlc == None:
			self.high = None
			self.low = None
			self.close = None
			return
		self.high = hlc.get('High',None)
		self.low = hlc.get('Low',None)
		self.close = hlc.get('Close',None)
	
	def calc_pivot(self):
		if self.high == None or self.close == None or self.low ==None:
			return None 
		p = (self.high + self.close + self.low)/3.0
		s1 = (p * 2) - self.high
		s2 = p  -  (self.high  -  self.low)
		r1 = (p * 2) - self.low
		r2 = p + (self.high - self.low)
		s3= p - (r2 - s2)
		r3 = (p - s2) + r2
		
		return {"Pivot" : round(p,2),
				"R1" : round(r1,2),
				"R2" : round(r2,2),
				"R3" : round(r3,2), 
				"S1"    : round(s1,2), 
				"S2"   : round(s2,2),
				"S3"   : round(s3,2),
				"Close" : round(self.close,2)
				}