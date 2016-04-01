from flask import render_template, request, send_file, Response, redirect
from app import app
from Dunkin.main import main
import time
from Dunkin.Update import UpdateData
#from forms import LoginForm
indexes ={'Nifty 50': 'CNX50'  ,'Nifty 500' : 'CNX500'}
FaceValue =['1','2','5','10']
MIS_SECTOR = {
    'CEMENT ':'CEMENT & CEMENT PRODUCTS',
    'FERTILISERS ' :'FERTILISERS & PESTICIDES',
    'MEDIA ':'MEDIA & ENTERTAINMENT'
    }

stock50 = main()
stock500 = main()
@app.route('/')
@app.route('/CNX50')
def nifty50():
    
    """form = LoginForm()
    if form.validate_on_submit():
         form.myfield.data,"yayayayayayay"""
    #stock = main()
    sector = request.args.get('sector', 'all')
    facevalue = request.args.get('facevalue', 'all')
    param = {
      "Sector" : sector,
      "Facevalue" : facevalue
    }
    if MIS_SECTOR.get(sector,None) is not None:
      param['Sector']= MIS_SECTOR.get(sector,"all")    
    
    if not stock50.stocklist:
      data = stock50.start_func('ind_niftylist.csv',param)
    else:
      print "here"
      data = stock50.get_stock_list(param)
    """data['INFY'].get_multiple_quarters()
    data['INFY'].get_multiple_half_years()
    data['INFY'].get_multiple_years()
    data['INFY'].get_multiple_five_years()
    data['INFY'].get_multiple_ten_years()
    """
    sectors = stock50.get_index_sectors()   
    return render_template("table.html",
                           index ='CNX50',
                           stocks = data,
                           indexes = indexes,
                           sectors = sectors,
                           FaceValue= FaceValue,
                           param = param,
                           )

@app.route('/CNX500')
def nifty500():
    sector = 'all'
    facevalue='all'
    sector = request.args.get('sector', 'all')
    facevalue = request.args.get('facevalue', 'all')
    param = {
      "Sector" : sector,
      "Facevalue" : facevalue
    }
    if MIS_SECTOR.get(sector,None) is not None:
      param['Sector']= MIS_SECTOR.get(sector,"all")    
    if not stock500.stocklist:
      data = stock500.start_func('ind_nifty500list.csv',param)
    else:
      print "here"
      data = stock500.get_stock_list(param)
    sectors = stock500.get_index_sectors()   
    return render_template("table.html",
                           index='CNX500',
                           stocks = data,
                           indexes=indexes,
                           sectors = sectors,
                           FaceValue= FaceValue,
                           param = param,
                           )

@app.route('/update')
def update():
  for ind in indexes:
    data = UpdateData('ind_niftylist.csv')
    if data.update():
      stock50.stocklist = {}
      stock500.stocklist ={}
  return redirect("/CNX50",)

