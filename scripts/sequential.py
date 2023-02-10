#!/usr/local/bin/python3

###################################################################################################
#                                                                                                 #
# SCRIPT FILE: sequential.py                                                                      #
# CREATION DATE: 02/02/2023                                                                       #
# HOUR: 10:10                                                                                     #
# DISTRIBUTION USED: UBUNTU                                                                       #
# OPERATIONAL SYSTEM: LINUX                                                                       #
#                                                                             DEVELOPED BY: BATES #
###################################################################################################
#                                                                                                 #
# SUMMARY: Execut the functions of the project                                                    #
#                                                                                                 #
###################################################################################################

# imports

from create_board import create_board
import subprocess

if __name__ == "__main__":
    create_board()
    print(subprocess.run(["python", "scripts/create_list.py"]))
    print(subprocess.run(["python", "scripts/create_cards.py"]))
    print(subprocess.run(["python", "scripts/update_field.py"]))
    print("Finishid!")