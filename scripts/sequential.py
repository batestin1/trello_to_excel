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
from create_list import create_list
from create_cards import create_card
from update_field import update_field
import time
import concurrent.futures

if __name__ == "__main__":
    create_board()
    create_list()
    create_card()
    update_field()