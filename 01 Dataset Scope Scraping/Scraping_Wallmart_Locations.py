# -*- coding: utf-8 -*-
"""
Script to scrape the Walmart website and obtain store locations


Created by: Joshua Blick
FIrst Version: 26/10/2020
"""
#import the required packages
from selenium import webdriver
import pandas as pd
import time

#define the google geocoding api key
api_key="AIzaSyDn-kD4UBvDq4-IeNmjzcc3Ubc8tZl_DGY"

#Define the address for the website 
store_loc_address="https://www.walmart.com/store/directory"

#Defining the element names which identify elements in the html
state_ele_name = "state-name"
city_ele_name = "city-name"
store_ele_name = "storeDetails"

##################################################################
###### Scraping the Wallmart website to get store locations ######
##################################################################

###### Defining functions to navigate around the website ######

def opendir_retstates(driver_var, store_loc_address, state_ele_name):
    """ Navigates to the top level by state directory and returns 
    a list of elements corresponding to the """
    #open the site showing the store directories
    driver_var.get(store_loc_address)
    #wait for the site to load
    time.sleep(3)
    #return a list of all the states
    return driver_var.find_elements_by_class_name(state_ele_name)


def openstate_returncities(driver_var, state_address, city_ele_name):
    """ Navigates to given state and returns list of elements
    of the cities in that state """
    #open the site for the specific state
    driver_var.get(state_address)
    #wait for the site to load
    time.sleep(3)
    #return a list of all the cities
    return driver_var.find_elements_by_class_name(city_ele_name)

def record_city_stores(driver_var, city_element, state_name, city_name, store_ele_name):
    """ 
    Navigates to a given city directory and returns a
    dataframe of all the store information """
    #click on the element for the given city
    city_element.click()
    #wait for the site to load
    time.sleep(4)
    #get a list of the elements for each store
    stores = driver_var.find_elements_by_class_name(store_ele_name)
    
    #initialise the list to hold the store details
    store_details = []
    
    #loop through the elements and appent the details to the dataframe
    for store_element in stores:
        # append the list of store deteils to the list
        store_details.append(store_element.text.split("\n")+[state_name]+[city_name])
    
    #return this 
    return store_details


###### Using the functions to navigate around the website ######

# establish a list in which we will accumulate the store deets
store_details_list=[]

#Open the web driver
driver=webdriver.Chrome()

#navigate to the store locator and return a list of the stores
states = opendir_retstates(driver, store_loc_address, state_ele_name)

#count the number of states
no_states = len(states)
#get a list of the states names
state_names = [state.text for state in states]

# we then loop through the states
for state_no, state_name in enumerate(state_names):
    #print the name of the state
    print("----------" + state_name + "----------")
    #navigate to the homepage to get a current list of elements
    state_eles = opendir_retstates(driver, store_loc_address, state_ele_name)
    state_eles[state_no].click()
    # get the state web address
    state_url = driver.current_url
    # open the state again and get a list of the city elements
    cities = openstate_returncities(driver, state_url, city_ele_name)
    #get the number of cities
    no_cities = len(cities)
    #get list of city names
    city_names = [city.text for city in cities]
    
    # so now we will loop through the cities and record the details
    for city_no, city_name in enumerate(city_names):
        #print the name of the city
        print(city_name)
        #reopen the state webpage to get current list of city elements
        cities = openstate_returncities(driver, state_url, city_ele_name)
        #collect the details of the stores in the city
        store_deets = record_city_stores(\
                                         driver, cities[city_no],\
                                             state_name, city_name, \
                                                 store_ele_name)
        #add to the list of stores:
        store_details_list = store_details_list + store_deets
    
driver.close()


#create a dataframe of the details
store_details = pd.DataFrame(store_details_list)

store_details.columns=['Store_Name', 'Address', 'City_State', 'Phone_no', 'Script_State', 'Script_City']

Relevant_Details = store_details[['Store_Name', 'Address', 'City_State']]

Relevant_Details.to_csv(r"C:\Users\paperspace\Documents\GitHub\satellite-car-counting\stores_complete.csv")



