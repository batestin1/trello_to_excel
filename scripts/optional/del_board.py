#!/usr/local/bin/python3

###################################################################################################
#                                                                                                 #
# SCRIPT FILE: create_board.py                                                                    #
# CREATION DATE: 02/02/2023                                                                       #
# HOUR: 10:10                                                                                     #
# DISTRIBUTION USED: UBUNTU                                                                       #
# OPERATIONAL SYSTEM: LINUX                                                                       #
#                                                                             DEVELOPED BY: BATES #
###################################################################################################
#                                                                                                 #
# SUMMARY: Creating a board on trello based on sheets of excel files                              #
#                                                                                                 #
###################################################################################################

# imports
import json
import pandas as pd
import requests
import time

# load configuration parameters from JSON files
with open('paramenters/keys.json') as f:
    keys = json.load(f)

with open('paramenters/paramenters.json') as f:
    parameters = json.load(f)

# set configuration variables
yourKey = keys['yourKey']
yourToken = keys['yourToken']
url_board = parameters['url_board']
url_base = parameters['url_base']
dir = parameters["dir_excel"]
field_get_id = parameters['field_get_id']
methods = parameters['methods']
worksheet = parameters['worksheet']

# load the Excel file into a pandas dataframe
df = pd.read_excel(dir,sheet_name=None)

def del_boards():
    # check if the worksheet exists in the Excel file
    if worksheet not in df:
        print(f"There is no worksheet with the name {worksheet}")
        return

    # get the ID of all boards with the same name on Trello
    url = f"{url_base}{field_get_id}&key={yourKey}&token={yourToken}"
    response = requests.get(url).json()
    board_ids = [item['id'] for item in response if item['name'] == worksheet]

    # delete all boards with the same name on Trello
    for board_id in board_ids:
        url = f"{url_board}{board_id}"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        query = {"key": yourKey, "token": yourToken}
        response = requests.delete(url, headers=headers, params=query)
        time.sleep(1)  # add delay to avoid hitting the Trello API rate limit

