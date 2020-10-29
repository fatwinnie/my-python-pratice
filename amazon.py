from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import os,sys

def Search(type_text):
    pageURL = 'https://www.amazon.com/'
    #search_URL = 'https://www.amazon.com/s?k=ultrawide+monitors&ref=nb_sb_noss_2'
    searchURL_template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'
    search_text = type_text
    search_term = search_text.replace(' ','+')
    #print(search_term)
    searchURL = searchURL_template.format(search_term) # put search_term into search_URL_template to replace {}
    #print(searchURL)

    return searchURL

    
    

def Get_Record(item):
    
    # list item 
       
    Item_Name = item.h2.a.text.strip()
    #print(Item_Name)

    Item_URL = 'https://www.amazon.com' + item.h2.a['href']
    #print(Item_URL)
    try:
        Price  = item.find('span','a-offscreen').text
        #print(Price)
    except AttributeError:
        Price = ''    
    
    try:
        Item_Star = item.find('i').text
        #print(Item_Star)
    except AttributeError:
        Item_Star = ''

    ReviewCount = item.find('span',{'class':'a-size-base','dir':'auto'}).text
    #print(ReviewCount)

    list_result = (Item_Name, Price, Item_Star, ReviewCount, Item_URL)
    return list_result
  

def main(product_name):

    searchURL = Search(product_name)

    driver = webdriver.Firefox()
    driver.get(searchURL)
    #print(driver.page_source)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    result = soup.find_all('div',{'data-component-type': 's-search-result'})

    records = []
    for item in result:
        record = Get_Record(item)
        records.append(record)
    
    # record as csv file
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
        writer.writerows(records)



if __name__ == '__main__':

    main('rtx 3080')
