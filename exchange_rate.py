import requests
from bs4 import BeautifulSoup 
import csv
import time 
import mysql.connector
from mysql.connector import Error

exchange_dic = {}
Time = []
Item = []
Price_buy = []
Price_sell = []
 

def main():    
    my_header = {
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'	
    }
    url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
    resp = requests.get(url, headers = my_header)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text,'lxml')

    # Get USD item (按照台銀頁面順序美金是0，港幣是1，以此類推)
    data_name = soup.find_all('div','hidden-phone print_show')
    #print(data_name[0].text.strip())
    name = data_name[0].text.strip()
    #Item.append(name)

    # Get price 
    data_price = soup.find_all('td','rate-content-sight text-right print_hide')
    # 美金 即期買入=data_price[0], 賣出=data_price[1]
    # 若是港幣 即期買入=data_price[2], 賣出=data_price[3]
    # print('本行即期賣出:',data_price[1].text) 本行即期賣出

    buying_price = float(data_price[1].text)
    selling_price = float(data_price[0].text)
    #Price_buy.append(buying_price)
    #Price_sell.append(selling_price)
    
    #賣出的價差
    result = selling_price - buying_price
    #print('%.2f' % result)
    price_GAP = '%.2f' % result
    print(price_GAP)

    #決定要不要賣
    if result < 1:
        print('Do not sell')

    # Get time
    current_time =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #Time.append(current_time)
    
    #exchange_dic['Time'] =  Time[0]
    #exchange_dic['Item'] = Item[0]
    #exchange_dic['Price_buy'] = Price_buy[0]
    #exchange_dic['Price_sell'] = Price_sell[0]
    #print(exchange_dic)
   
    #USD_info = (exchange_dic['Time'],exchange_dic['Item'],exchange_dic['Price_buy'],exchange_dic['Price_sell'],price_GAP)   
    USD_info = (current_time,name,buying_price,selling_price,price_GAP)
    print(USD_info)
    Write_to_csv(USD_info)
    Write_to_DB(current_time,name,buying_price,selling_price,price_GAP)

    
def Write_to_csv(getInfo):
    with open('usd.csv','a',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Time','Item','Price_Buy','Price_Sell','GAP'])      
        writer.writerow(getInfo)
    
def Write_to_DB(time,item,buy,sell,priceGAP):
    # write to DB
    conn = mysql.connector.connect(      
    host='localhost', 
    database='homework', 
    user='root',     
    password='2033',  
    charset='utf8') 

    cursor = conn.cursor()
    try:
        sql = "INSERT INTO exchange_rate (Time,Item,Now_buying,Now_selling,gap) VALUES (%s,%s,%s,%s,%s);"
        value = (time,item,buy,sell,priceGAP)
        cursor.execute(sql,value)
    except Error as e:
        print("Error:",e)

    conn.commit()
    conn.close()
        
if __name__ == '__main__':

    main()    
    


