# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 10:49:30 2022

@author: Supriya Malla
"""

import requests
from bs4 import BeautifulSoup
import random
import pandas as pd


A = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        )
Agent = A[random.randrange(len(A))]
headers = {'user-agent': Agent}

#vendors are just company names/individuals you want to look for
vendor_list=[] # Empty list to read all vendor names
vendor_link=[] #Empty list to store all vendor profile links
vendor_state=[] # Empty list to read state to further refine google searches
vendor_type=[] # Empty list to read two types of vendors Ind (Individual) or ORG (Organization)

vendor_df=pd.read_excel('Write the path of your file.xlsx')

for index, row in vendor_df.iterrows():    
    url = 'https://google.com/search?q=' + str(row['Vendor Name']) + ' ' +str(row['Vendor State']) + ' '+'Linkedin' #Refining the search to the company/individual name by adding state to the search
    #you can also add other variables to further optimize the search
    r = requests.get(url)
  
    soup = BeautifulSoup(r.text, 'lxml')
    
    for link in soup.find_all('a', href=True):
        data = link.get('href')
       
        if('url' in data): #if the data variable contains word "URL" only getting that information
            data=data.split('=', 1)[1]
            data=data.split('&', 1)[0]
            #df=pd.DataFrame({'Vendor Name': [vendor], 'Vendor Link': [data]})
            vendor_list.append(row['Vendor Name'])
            vendor_state.append(row['Vendor State'])
            vendor_type.append(row['Vendor Type']) #Vendor Type is whether the vendor is an individual or an organization
            vendor_link.append(data)
    
            break
df = pd.DataFrame(list(zip(vendor_list,vendor_state,vendor_type, vendor_link)),columns =['Vendor Name', 'Vendor State', 'Vendor Type','Vendor Link'])

df.to_csv('Enter your file name.csv', index=False)
