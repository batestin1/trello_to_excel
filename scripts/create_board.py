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
import requests
import pandas as pd
from trello import TrelloClient
import tqdm
import json
from optional.del_board import del_boards
import time

parKeys=open('paramenters/keys.json')
parameter = open('paramenters/paramenters.json')
data_parm = parameter.read()
data = parKeys.read()
content = json.loads(data)
content_parm = json.loads(data_parm)
yourKey = str(content['yourKey'])
yourToken = str(content['yourToken'])
url_board = content_parm['url_board']
url_base = content_parm['url_base']
dir = content_parm["dir_excel"]
field_get_id = content_parm['field_get_id']
methods = content_parm['methods']
worksheet = content_parm['worksheet']

# Loads the Excel file into a dataframe
df = pd.read_excel(dir)

# Connects to the Trello API

client = TrelloClient(
    api_key=yourKey,
    token=yourToken
)


def create_board():
    df = pd.read_excel(dir, sheet_name=None)
    values = df.keys()
    name_list = list(values)

    # Check if the worksheet exists
    if worksheet in name_list:
        boards = client.list_boards()
        name_board = [board.name for board in boards]

        # Check if the board already exists
        if worksheet in name_board:
            print(f"The board {worksheet} already exists!")
            choiced = input("Do you want to update the information?[Y/N] ")[0].lower()
            if choiced == 'y':
                del_boards()
                time.sleep(1)
                client.add_board(worksheet, default_lists=False)
                id_board = client.list_boards()
                board = next(i for i in client.list_boards() if i.name == worksheet)
                df = pd.read_excel(dir, sheet_name=worksheet)
                a = df.iloc[0].to_dict()
                columns = list(a.keys())
                values = list(a.values())
                headers = {"Accept": "application/json", "Content-Type": "application/json"}
                query = {"key": yourKey, "token": yourToken}
                for col in columns:
                    url = f"{url_base}customFields"
                    payload = json.dumps({
                        "idModel": board.id,
                        "name": col,
                        "type": "text",
                        "pos": "top",
                        "modelType": "board",
                        "display_cardFront": True,
                        "isSuggestedField": True
                    })
                    response = requests.request(methods[1],url,data=payload,headers=headers,params=query)
                print(f"Board {worksheet} successfully created")
            else:
                print("OK then")
        else:
            client.add_board(worksheet, default_lists=False)
            id_board = client.list_boards()
            board = next(i for i in client.list_boards() if i.name == worksheet)
            df = pd.read_excel(dir, sheet_name=worksheet)
            a = df.iloc[0].to_dict()
            columns = list(a.keys())
            values = list(a.values())
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            query = {"key": yourKey, "token": yourToken}
            for col in columns:
                url = f"{url_base}customFields"
                payload = json.dumps({
                    "idModel": board.id,
                    "name": col,
                    "type": "text",
                    "pos": "top",
                    "modelType": "board",
                    "display_cardFront": True,
                    "isSuggestedField": True
                })
                response = requests.request(methods[1],url,data=payload,headers=headers,params=query)
            print(f"Board {worksheet} successfully created")
    else:
        print("There is no worksheet with this name")
