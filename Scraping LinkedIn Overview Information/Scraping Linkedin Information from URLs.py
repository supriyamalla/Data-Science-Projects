# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 08:22:48 2022

@author: Supriya Malla
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
import pandas as pd

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
vendor_name=[]
vendor_short_desc=[]
vendor_summary_info=[]
vendor_overview=[]
vendor_link=[]
vendor_df=pd.read_csv('Enter your file name.csv') #This is the file name which has the list of Linkedin URLs (which you got from the previous code)


final_vendor_link=list(vendor_df['Vendor Link'])
print(final_vendor_link)
# This instance will be used to log into LinkedIn
  
# Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")
  
# waiting for the page to load
time.sleep(5)
  
# entering username
username = driver.find_element(By.ID, "username")
  
# Enter Your Email Address
username.send_keys("Enter your mail ID")  
  
# entering password
pword = driver.find_element(By.ID, "password")
  
# Enter Your Password
pword.send_keys("Enter your password")        
  
# Clicking on the log in button
driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()


for index, row in vendor_df.iterrows():
    if(row['Vendor Type']=='ORG'):
        row['Vendor Link'] = str(row['Vendor Link']) + '/about' #Organizations have an "about" page but Individuals don't
        #print(vendor_df['Vendor Link'])

#Below code will help you extract the webpage information
def extract_till_end():
    start = time.time()
    initialScroll = 0
    finalScroll = 1000
    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        initialScroll = finalScroll
        finalScroll += 1000
        time.sleep(3)
        # You can change it as per your needs and internet speed
      
        end = time.time()
        if round(end - start) > 20:
            break
    
for index, row in vendor_df.iterrows():
    try:
        
        driver.get(row['Vendor Link'])
        if(driver.current_url=='https://www.linkedin.com/feed/'):
            continue
        # will be used in the while loop
        extract_till_end()
          
    
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        extract_till_end()
        
        #Org and Ind have different page structures/elements
        if(row['Vendor Type']=='ORG'):
           
            intro = soup.find('div', {'class': 'block mt2'})
            name_loc = intro.find("h1")
            short_desc = intro.find("p", {'class': 'org-top-card-summary__tagline t-16 t-black'})
            summary_info = intro.find("div", {'class': 'org-top-card-summary-info-list__info-item'})
            overview = soup.find("section", {"class": "artdeco-card p5 mb4"})
            overview_des=overview.find("p", {"class": "break-words white-space-pre-wrap mb5 text-body-small t-black--light"})
           
            
        elif(row['Vendor Type']=='IND'):
            intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
            name_loc = intro.find("h1")
            short_desc = intro.find("div", {'class': 'text-body-medium break-words'})
            
            summary_info = soup.find("h2", {'class': 'pv-text-details__right-panel-item-text hoverable-link-text break-words text-body-small inline'})
            overview_des = soup.find('div', {'class': 'pv-shared-text-with-see-more t-14 t-normal t-black display-flex align-items-center'})
            print("else condition ends")
            
        
         
        # Extracting the Name
        name = name_loc.get_text().strip()
        vendor_name.append(name)
       
        vendor_link.append(row['Vendor Link'])
        #The below IF conditions are to avoid any errors
        if(short_desc!=None):
            short_desc = short_desc.get_text().strip()
            vendor_short_desc.append(short_desc)
        else:
            vendor_short_desc.append(' ')
       
        if(summary_info!=None):
            summary_info = summary_info.get_text().strip()
            vendor_summary_info.append(summary_info)
        else:
            vendor_summary_info.append(' ')
        if(overview_des!=None):
            overview_data = overview_des.get_text().strip()
            print("Overview_des -->", overview_data)         
            vendor_overview.append(overview_data)
        else:
            vendor_overview.append(' ')
    except:
        
        continue # a way to mitigate any errors
            
df = pd.DataFrame(list(zip(vendor_name, vendor_link,vendor_short_desc,vendor_summary_info, vendor_overview)),columns =['Vendor Name', 'Vendor Link','Short Description', 'Summary Info','Vendor Overview'])
df.to_csv('Your final file name.csv', index=False)
   
