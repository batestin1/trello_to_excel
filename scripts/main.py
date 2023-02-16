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
from keys import keys, change_excel
from excel_to_trello import create_board
from trello_to_excel import to_excel
from optional.del_board import del_boards


if __name__ == "__main__":
    while True:
        choice = int(input("""
        What do you want to do:
        [1] - Excel To Trello
        [2] - Trello To Excel
        [3] - Del Board on Trello
        R: """))
        if choice == 1:
            keys()
            change_excel()
            create_board()
            break
        elif choice == 2:
            keys()
            change_excel()
            to_excel()
            break
        elif choice == 3:
            keys()
            change_excel()
            del_boards()
            break
        else:
            print("Invalid choice. Please choose a valid option.\n")

