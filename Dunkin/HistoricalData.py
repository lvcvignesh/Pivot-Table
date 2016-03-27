# File to Fetch Historical Data of 
# Sadly, they discontinued the service for Yahoo India Finance. So, html data is scrapped instead.
import urllib2
import time
BASE_URL = 'http://ichart.finance.yahoo.com/table.csv?s='

def get_content(symbol,start,end):
    """ 
    """
    # Currently, only BSE, NSE will be added.
    symbol_url = '%s%s.NS&d=%s&e=%s&f=%s&g=d&a=%s&b=%s&c=%s&ignore=.csv' % (BASE_URL, symbol, 
                        int(end[1])-1,end[0],end[2],int(start[1])-1,start[0],start[2])
    response = urllib2.urlopen(symbol_url)
    html = response.read()
    return html

def get_quote(symbol):
    """
    Returns today's stock price
    """  

def get_previous_close(symbol):
    """
    Returns yesterday's closing price
    """ 

def get_opening_quote(symbol):
    """
    Returns today's opening stock price
    """

def get_todays_change(symbol):
    """
    Returns change in stock price today
    """    

def get_todays_max(symbol):
    """
    Returns maximum price for today
    """   

def get_todays_min(symbol):
    """
    Returns minimum price for today
    """   
def get_volume(symbol):
    """
    Returns total volume of stock transection
    """
def get_summary(symbol):
    """
    Returns dict with stock summary
    """
    """
        def get_last_quote():

            def get_week_quote():

                def get_month_quote():

                    def get_3month_quote():

                        def get_quarter_quote():

                            def get_half_yearly_quote():

                                def get_yearly_quote():

                                    def get_5yearly_quote():

                                        def get_10year_quote():

                                            def get_max_quote():
        