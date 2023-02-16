#!/usr/local/bin/python3

###################################################################################################
#                                                                                                 #
# SCRIPT FILE: init.py                                                                            #
# CREATION DATE: 02/02/2023                                                                       #
# HOUR: 10:10                                                                                     #
# DISTRIBUTION USED: UBUNTU                                                                       #
# OPERATIONAL SYSTEM: LINUX                                                                       #
#                                                                             DEVELOPED BY: BATES #
###################################################################################################
#                                                                                                 #
# SUMMARY: Init the project                                                                       #
#                                                                                                 #
###################################################################################################

# imports
import json
import requests
import os

path = "database/"

for filename in os.listdir(path):

    if filename.endswith(".xlsx"):

        if filename != "dataset.xlsx":
            os.rename(os.path.join(path, filename), os.path.join(path, "dataset.xlsx"))
            print(f"File {filename} renamed to dataset.xlsx")

        else:
            print("The file already has the name dataset.xlsx")

    else:
        print(f"File {filename} is not an Excel file") 
from keys import keys
from excel_to_trello import create_board
from trello_to_excel import to_excel
from optional.del_board import del_boards


while True:
    choice = int(input("""
    What do you want to do:
    [1] - Excel To Trello
    [2] - Trello To Excel
    [3] - Del Board on Trello
    R: """))
    if choice == 1:
        keys()
        create_board()
        break
    elif choice == 2:
        keys()
        to_excel()
        break
    elif choice == 3:
        keys()
        del_boards()
        break
    else:
        print("Invalid choice. Please choose a valid option.\n")

