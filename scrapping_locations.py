import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import time
import re

def scrapper(hastags):
    """Functions scraps google to try to find instagram location codes from the names of the places

    Args:
        hastags (pandas.DataFrame): Dataframe with a single column called location. This column has the name of the places whose location codes we need to find

    Returns:
        hastags (pandas.DataFrame): Input dataframe with a new column url where the location code may be found
    """
    hastags["url"]=" "
    driver=webdriver.Firefox()
    for i in range(len(hastags)):
        loc=hastags.iloc[i]["Location"]
        loc=" ".join(re.findall("[A-Z][^A-Z]*",loc))
        print(loc)
        driver.get("site:https://www.instagram.com/explore/locations/?hl=es"+loc)
        try:
            driver.find_element(By.CSS_SELECTOR,"#W0wltc > div:nth-child(1)").click()
            driver.find_element(By.CSS_SELECTOR,"#rso > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1) > h3:nth-child(2)").click()
            url=driver.current_url
            print(url)
            hastags.loc[i]["url"]=url
            time.sleep(10)
        except:
            try:
                driver.find_element(By.CSS_SELECTOR,"#rso > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1) > h3:nth-child(2)").click()
                url=driver.current_url
                hastags.loc[i]["url"]=url
                print(url)
                time.sleep(10)
            except:
                time.sleep(10)    
                continue

        
        
    return hastags

if __name__ == "__main__":


    df=pd.read_csv("failed_places.txt",names=["Location"])
    df=scrapper(df)
    print(df)
    fun= lambda x : [int(s) for s in x.split("/") if s.isdigit()] #to retrive the code from the url
    lista=list(map(fun,df.url))
    replace= lambda y: str(y).replace("[","").replace("]","")
    newlist=list(map(replace,lista))
    df["codes"]=newlist
    df.to_csv("result.csv",index=False)
    subdf=df[df.codes!=""] #we select only the rows where a location code could be found
    #This codes are saved in a file
    with open('location_codes.txt', 'w') as f:
        for line in subdf.codes:
            f.write("%s\n" % line)

    #In the same manner, those places where a location code could not be found, are also saved. Maybe we can try again
    
    subdf=df[df.codes==""]
    with open('failed_places.txt', 'w') as f:
        for line in subdf.Location:
            f.write("%s\n" % line)
            

    
