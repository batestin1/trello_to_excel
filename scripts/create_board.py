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
    boards = client.list_boards() 
    if worksheet in name_list:
        name_board = []
        for board in boards:
            name_board.append(board.name)
        if worksheet in name_board:
            print(f"The board {worksheet} already exist!")
        else:
            client.add_board(worksheet,default_lists=False)
            id_board = client.list_boards()
            for i in client.list_boards():
                if i.name == worksheet:
                    df = pd.read_excel(dir, sheet_name=worksheet)
                    a = df.iloc[0].to_dict()
                    columns_ = list(a.keys())
                    values_ =list(a.values())
                    for col in columns_:
                        for val in values_:
                            url = f"{url_base}customFields"
                            headers = {"Accept": "application/json", "Content-Type": "application/json"}
                            query = {"key": yourKey, "token": yourToken}
                            payload = json.dumps({
                                "idModel": i.id,
                                "modelType": "board",
                                "name": col,
                                "option": str(val),
                                "type": "checkbox",
                                "pos": "bottom",
                                "display_cardFront": "true"}
                            )
                            response = requests.request(
                                methods[1],
                                url,
                                data=payload,
                                headers=headers,
                                params=query
                            )
            print(f"Board {worksheet} successfully created")
    else:
        print("There is no worksheet with this name")

