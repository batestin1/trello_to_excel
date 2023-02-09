#!/usr/local/bin/python3

###################################################################################################
#                                                                                                 #
# SCRIPT FILE: keys.py                                                                            #
# CREATION DATE: 02/02/2023                                                                       #
# HOUR: 10:10                                                                                     #
# DISTRIBUTION USED: UBUNTU                                                                       #
# OPERATIONAL SYSTEM: LINUX                                                                       #
#                                                                             DEVELOPED BY: BATES #
###################################################################################################
#                                                                                                 #
# SUMMARY: Validated key and token acess of trello api                                            #
#                                                                                                 #
###################################################################################################

# imports

import json
import requests



def keys():

    while True:
        yourKey = str(input("Your Key acess: "))
        if len(yourKey) != 32:
            print("There something wrong with your key, please try again!")
        else:
            print("Key acess saved!")
            break
    while True:
        yourToken = str(input("Your Token acess: "))
        if len(yourToken) != 76:
            print("There something wrong with your token, please try again!")
        else:
            print("Token acess saved!")
            break
    
    #validation key connection
    link = f"""https://api.trello.com/1/members/me/boards?fields=name,url&key={yourKey}&token={yourToken}"""
    response = requests.get(link)
    if response.status_code == 200:
        print("Access Key and Token it is authenticated and validated!")
        output = open("paramenters/keys.json", "w")
        df = {
                "yourKey": yourKey,
                "yourToken": yourToken
            }
        json.dump(df,output,allow_nan=True,indent=True,separators=(',',':'))
    else:
        print("Access Key and Token no It is authenticated and validated!")
        print("review your access")

        

