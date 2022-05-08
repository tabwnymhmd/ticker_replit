from os import remove
from threading import Thread
from replit import web,clear
from flask import Flask,request
from seleniumwire.webdriver import Chrome,ActionChains,ChromeOptions

ticker = 'ADAUSDT'
ticker_datas = '[]'
default_period = '15'

options = ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def run () :

    app = Flask(__name__)

    @app.route('/')
    def index () :
        global ticker_datas
        clear()
        return ticker_datas

    @app.route('/period')
    def time_period ():return open('period.txt').read()

    @app.route('/interval')
    def intervl () :
        period = request.args.get('period',default_period,str)
        if period in ['1','3','5','15','30','1h','2h','4h','1d','1w','1m'] : 
            with open('period.txt','w') as new_period:new_period.write(period);new_period.close()
            actions.pause(0.2).send_keys(f'{period}\ue007').perform()
            return 'time period changed to ' + period
        else:return 'No time period ' + period

    @app.route('/screenshot')
    def photo () :
        table.screenshot('chart.png')
        chart = str(open('chart.png','rb').read())
        remove('chart.png')
        return chart

    web.run(app)

def ticker_data (ticker):

    global default_period,ticker_datas,options,driver,table,actions

    data = lambda x:float(driver.find_element_by_xpath(x).text)
    datas = lambda *x:str(list(map(data,x)))
	
    driver = Chrome(chrome_options=options)
    actions = ActionChains(driver)

    driver.header_overrides={'cookie':'_ga=GA1.2.1695615786.1641679997; __gads=ID=5bbe996c698eb7ad:T=1641971736:S=ALNI_MY-Zp9kiqm1wtOznyawKnUKgiRcLQ; will_start_trial=1; backend=prod_backend; device_t=T3V5c0FROjEsQjM0ZEFnOjAsSkg0ZEFnOjAsUTM0ZEFnOjAsVVg0ZEFnOjA.XpO4L-UhONZud3hv4N4fmX-XfP-DYBgA1Shk06h_78s; _gid=GA1.2.1872863008.1650975943; __gpi=UID=000004c4d2397adf:T=1649940605:RT=1651028422:S=ALNI_MbIZ-x02N_oOy8t5ChJ9d4lXspv-g; _sp_ses.cf1a=*; sessionid=px7w4rkby1naqka6uzylvyvzrh1exqra; etg=35b4204f-1509-4231-b410-34f57e35b0ba; cachec=35b4204f-1509-4231-b410-34f57e35b0ba; png=35b4204f-1509-4231-b410-34f57e35b0ba; tv_ecuid=35b4204f-1509-4231-b410-34f57e35b0ba; _gat_gtag_UA_24278967_1=1; _sp_id.cf1a=c80ec655-04d3-4547-86ef-bfbfb9838e96.1641679996.143.1651069037.1651037112.47f9e91c-ef55-49ff-932f-066f7c35e227'}
    driver.set_window_size(1900,1400)

    driver.get('https://www.tradingview.com/chart/K9CKq0sj/')

    table = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div/table')

    while True :
        try:driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div[2]/div[1]').click()
        except:continue
        try:driver.find_element_by_xpath('/html/body/div[6]/div/div/div[2]/div/div[2]/div[1]/input').send_keys(f'BINANCE:{ticker}\n')
        except:continue
        else:break

    try:period = open('period.txt').read()
    except:period=open('period.txt','w');period.write(default_period);period.close()
    actions.move_by_offset(50,700).pause(0.3).send_keys(f'{period}\ue007').pause(3).perform()
    
    while True:
        try:ticker_datas=datas('/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[5]/td[2]/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div')
        except:pass
 
Thread(target=run).start()
Thread(target=ticker_data,args=[ticker]).start()