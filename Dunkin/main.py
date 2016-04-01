"""

TODO : General Features 

1 . Fetching Historical Data
2.  Fetching of INDICES
3.  Organising data. files or likewise

TODO : Requirements

1. Pivot
2. Graphs
3. StockScreener 
"""
from nsetools import Nse
from pprint import pprint
from StockData import StockData
from datetime import date
from Update import UpdateData


"""app = UpdateData('ind_niftylist.csv')
app.update_index()
API_KEY ='7zTazsysxctwCz4jsH8h'
str = 'GTLINFRA'
nse =Nse()
count = 0 
"""
all_String = 'all'
class main:

	def __init__(self):
		self.sectors = {}
		self.stocklist = {}
	def start_func(self, index, param = None):
		data = UpdateData(index)
		count = 0
		stocklist ={}
		if param is not None:
			facevalue = param.get('Facevalue')
			sector = param.get('Sector')
		with open(index) as myfile:
			for line in myfile:
				if count is not 0: 
					line = line.split(',')
					try:
						#data.update_hlc(line[2])
						stock = StockData(line[2],data,line[1])
						if self.sectors.get(line[1]) is None:
							self.sectors[line[1]]=line[1]
						#stocklist[stock.stock] = stock
						self.stocklist[stock.stock] = stock
	
					except:
						print line[2]
						continue
					
				else : count = 1
		return self.stocklist

	def get_stock_list(self, param = None):
		stocklist = {}
		if param is not None:
			facevalue = param.get('Facevalue')
			sector = param.get('Sector')
		for key,stock in self.stocklist.iteritems():
			if facevalue is not all_String and sector is not all_String:
				if (stock.get_face_value() == float(facevalue)) and (stock.sector == sector):
					stocklist[stock.stock] = stock 
			elif facevalue is not all_String:
				if stock.get_face_value() == float(facevalue) :
					stocklist[stock.stock] = stock
			elif sector is not all_String:
				if stock.sector == sector:
					stocklist[stock.stock] = stock
			else: 
				return self.stocklist
		return stocklist

	def get_index_sectors(self):
		return self.sectors

"""#pprint(stock.get_all_pivot(stock.pivot_diff))
#stock = StockData(str,data)
#pprint(stock.get_content())

	#pprint(stock.file.read_from_dict())"""