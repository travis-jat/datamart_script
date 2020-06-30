#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:30:20 2020

@author: travishartman
"""

import csv
import sys
import datetime
from datetime import datetime

# read in the csv file
#csv_file = open(sys.argv[1], 'r')

csv_file = open('/Users/travishartman/Desktop/datamart/schema/verifier/datamart_schema.csv')
#list to hold all the dates
dater=[]
reader = csv.reader(csv_file)
headers_list = next(reader, None)

for a in csv.reader(csv_file, delimiter=','):
    dater.append(a[0])

#### FUNCTIONS ####

#verify that 'country' is in the header
def verify_country(headers_list):

    country = False
    
    if "country" in headers_list:
        country = True
        
    return country    

# Verify that 'timestamp' is in the header
def verify_timestamp(headers_list):
    
    stamp = False
    
    if "timestamp" in headers_list:
        stamp = True
        
    return stamp

# Verify date FORMAT
def verify_timestamp_format(dt_str):
    
    last_one = dt_str[-1]
    
    if last_one == "Z" or last_one == "z":
        dt_str = dt_str[:-1]

    try:
        datetime.fromisoformat(dt_str)
    except:
        return False
    
    return True

def get_features(headers_list):
    
    feature_list=[]
    
    for header in headers_list:
        if "_name" in header:
            feature_list.append(header.split("_name")[0])
    
    return feature_list

#Function to add key,value pairs without overwriting existing info
def set_key(dictionary, key, value):
    
    if key not in dictionary:
        dictionary[key] = value
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]

# Create dictionary to add k.v of features and any associated atrributes for that feature
def get_feature_attr(feature_list, headers_list):
    
    header_dict ={}
    
    for feature in feature_list:
        for thing in headers_list:
            if feature in thing:
                set_key(header_dict, feature, thing)
                 
    return header_dict

# Check that 'description' is in the dataset for each feature
def verify_description(header_dict):
    
    list_bool=[]
    
    for key in header_dict:
        temp_bool = False
        temp_list = header_dict[key]
        
        for thing in temp_list:
            if 'description' in thing:
                temp_bool = True
        
        list_bool.append([key, temp_bool])
        
    return list_bool 

# Check for and return any differences in the dateset header versus the header columns that are accounted for
def the_accounter(headers_list):
    
    not_accounted_for = []
    if verify_timestamp(headers_list) == True:
        not_accounted_for.append("timestamp")
    if verify_country(headers_list) == True:
        not_accounted_for.append("country")
    
    # get all the feautures and attributes
    things = get_feature_attr(get_features(headers_list), headers_list)
    
    for key in things:
        for thing in things[key]:
            not_accounted_for.append(thing)
        
    return (list(set(headers_list) - set(not_accounted_for)))

#Put is all together
def wrapperitup(headers_list, dater):
    
    #populate with function outputs
    country = verify_country(headers_list) 
    time_stamp = verify_timestamp(headers_list)
    features_list = get_features(headers_list)
    header_dict = get_feature_attr(features_list, headers_list)
    descr_list = verify_description(header_dict)
    diff = the_accounter(headers_list)
    
    #features_in_set => [test if any features, number of features, list of features]
    
    holder_of_meta = {'qualifier': header_dict,
                      'country_in': None, 
                      'timestamp_in': None, 
                      'timestamp_format': None, 
                      'features_in_set': [None,0,None], 
                      'desc_for_feature':None,
                      'header_diff': diff}
    
    # COUNTRY CHECK --> Boolean
    holder_of_meta['country_in'] = country   
    
    # TIMESTAMP CHECK --> Boolean
    holder_of_meta['timestamp_in'] = time_stamp
    
    #  TIME FORMAT--> Boolean
    list_date_bool = []
    for t in dater:
        list_date_bool.append(verify_timestamp_format(t))
    
    holder_of_meta['timestamp_format'] = all(list_date_bool)    
    
    #  CHECK FOR the NAME TAG--> feature_list
    if len(features_list) > 0:
        holder_of_meta['features_in_set'][0] = True
        holder_of_meta['features_in_set'][1] = len(features_list) 
        holder_of_meta['features_in_set'][2] = features_list
    
    #  CHECK FOR DESCRIPTION --> header_dict
    holder_of_meta['desc_for_feature'] = descr_list
    
    
    return holder_of_meta

# Displacy the results
def displayer(holder_of_meta):

    # Lists to hold the fails/good to gos
    success = []
    fail = []
    warn = []
    
    print('\n')
    print("Checking your file for schema compliance..." +  "\r\n")
    
    
    # Check if there are any features first!
    temp = holder_of_meta['features_in_set']
    temp_q = holder_of_meta['qualifier']

    if temp[1] == 0:
        fail.append('Failed scan for features --> NO FEATURES FOUND')
        fail.append('Update your feature header to include the "_name" tag')
        fail.append('Example: change crop_price to crop_price_name')
    # Ok, there are features so run the rest of the verification
    else:
        for key in temp_q:
            
            if isinstance(temp_q[key], list):
                print(f"Found Feature: {key} with {len(temp_q[key])-1} qualifier(s)")
                for q in temp_q[key][1:]:
                    print(f"    Qualifier: {q}")
            else:
                print(f"Found Feature: {key} with ZERO qualifiers")
                
        print('\n')
        print(f"Found {temp[1]} total feature(s)") 	
        print(f"If you have more than {temp[1]} feature(s), verify your feature has the '_name' tag" + '\r\n')

        yes = 'Passed: '
        nope = 'FAILED VERIFICATION: ' 
        maybe = "Warning: "
        v = " verified"

        schema_nulls = ['latitude', 'longitude', 'polygon', 'admin_1', 'admin_2', 'admin_3']

        temp = holder_of_meta['header_diff']
        if temp == True:
            success.append(yes + 'header accounting' + v)
        else:
            for thing in temp:
                if thing not in schema_nulls:
                    warn.append(maybe + "--> Verify that '" + thing + "' column header is correct")  
        
        temp = holder_of_meta['country_in']
        if temp == True:
            success.append(yes + 'country' + v)
        else:
            fail.append(nope + "--> 'country' is a required column header")   

        temp = holder_of_meta['timestamp_in']
        if temp == True:
            success.append(yes + 'timestamp' + v)
        else:
            fail.append(nope + "--> 'timestamp' is a required column header")         

        temp = holder_of_meta['timestamp_format']
        if temp == True:
            success.append(yes + 'timestamp format' + v)
        else:
            fail.append(nope  + "-->  Format for 'timestamp' must be ISO 8601")
       
        temp = holder_of_meta['desc_for_feature']
        for t in temp:
            if t[1] == True:
                success.append(yes +"Description verified for feature: " + t[0])
            else:
                fail.append(nope + '--> No Description found for feature: ' + t[0])
    
    # Print out the results:  
    if success != []:
        for s in success:
            print(s)
        print('\n')

    if warn != []:
        for w in warn:
            print(w)
        print('***If your column header is correct, ignore the warning; otherwise change the associated column header')
        print('\n') 

    if fail != []:
        for f in fail:
            print(f)     

    if fail == [] and warn == []: 
        print("          Congratulations, your file is schema-compliant")
        print('\n') 

    if fail != []:
        print('\n')
        print("          YOUR FILE IS NOT SCHEMA-COMPLIANT. CORRECT THE VERIFICATION FAILURES AND RE-RUN")
        print('\n')        


# call functions and display results
verification_results = wrapperitup(headers_list, dater)
displayer(verification_results)


