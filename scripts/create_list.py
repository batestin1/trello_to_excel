#!/usr/local/bin/python3

###################################################################################################
#                                                                                                 #
# SCRIPT FILE: create_list.py                                                                     #
# CREATION DATE: 02/02/2023                                                                       #
# HOUR: 10:10                                                                                     #
# DISTRIBUTION USED: UBUNTU                                                                       #
# OPERATIONAL SYSTEM: LINUX                                                                       #
#                                                                             DEVELOPED BY: BATES #
###################################################################################################
#                                                                                                 #
# SUMMARY: Creating a list on trello based on sheets of excel files                               #
#                                                                                                 #
###################################################################################################

# imports

import json
import pandas as pd
from trello import TrelloClient

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
df = pd.read_excel(dir)
client = TrelloClient(
    api_key=yourKey,
    token=yourToken
)
def create_list():
    df = pd.read_excel(dir, sheet_name=None)
    values = df.keys()
    name_list = list(values)
    if worksheet in name_list:
        df = pd.read_excel(dir, sheet_name=worksheet)
        unique_values = df["Current Week Action"].unique()
        for title in unique_values:
            boards = client.list_boards()
            for board in boards:
                if board.name == worksheet:
                    listId = client.get_board(board.id)
                    lists = listId.all_lists()
                    if title not in [l.name for l in lists]:
                        board.add_list(f"{title}",pos='bottom')
        print("List built successfully")
    else:
        print("There is no worksheet with this name")

