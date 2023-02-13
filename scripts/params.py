#!/usr/local/bin/python3

###################################################################################################
#                                                                                                 #
# SCRIPT FILE: params.py                                                                          #
# CREATION DATE: 02/02/2023                                                                       #
# HOUR: 10:10                                                                                     #
# DISTRIBUTION USED: UBUNTU                                                                       #
# OPERATIONAL SYSTEM: LINUX                                                                       #
#                                                                             DEVELOPED BY: BATES #
###################################################################################################
#                                                                                                 #
# SUMMARY: writing the paramenters                                                                #
#                                                                                                 #
###################################################################################################

# imports
import json
import os
import pandas as pd

def parameters():
    with open('paramenters/paramenters.json') as f:
        data = json.load(f)

    while True:
        dir_excel = input("Enter the path and name of your excel file: ")
        if not dir_excel.endswith(".xlsx"):
            print("File is not an excel file. Please insert a xlsx file.")
            continue
        if not os.path.exists(dir_excel):
            print("File does not exist. Please insert a valid file.")
            continue
        break
        
    worksheet = input('Enter the name of the sheet you want to use: ')
    list = input("Enter the name of the list you want to use: ")
    card = input("Enter the name of the cards you want to use: ")
    data['dir_excel'] = dir_excel.replace("\\", "/")
    data['worksheet'] = worksheet
    data['list'] = list.title()
    data['card'] = card.title()


    with open('paramenters/paramenters.json', 'w') as f:
        json.dump(data, f, indent=4)

