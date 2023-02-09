#!/usr/local/bin/python3

###################################################################################################
#                                                                                                 #
# SCRIPT FILE: create_cards.py                                                                    #
# CREATION DATE: 02/02/2023                                                                       #
# HOUR: 10:10                                                                                     #
# DISTRIBUTION USED: UBUNTU                                                                       #
# OPERATIONAL SYSTEM: LINUX                                                                       #
#                                                                             DEVELOPED BY: BATES #
###################################################################################################
#                                                                                                 #
# SUMMARY: Creating a card on trello based on sheets of excel files                               #
#                                                                                                 #
###################################################################################################

# imports
import pandas as pd
from trello import TrelloClient
import json
import colorama

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

client = TrelloClient(
    api_key=yourKey,
    token=yourToken
)


def create_card():
    boards = client.list_boards()
    for board in boards:
        if board.name == worksheet:
            client.get_board(board.id)
            lists = board.all_lists()
            for i in lists:
                df = pd.read_excel(dir, sheet_name=None)
                values = df.keys()
                name_list = list(values)
                if worksheet in name_list:
                    df = pd.read_excel(dir, sheet_name=worksheet)
                    for index,row in df.iterrows():
                        if row['Current Week Action'] == i.name:
                            card_name = row['Practitioner Notes ID']
                            cards = i.list_cards()
                            card_names = [c.name for c in cards]
                            if card_name not in card_names:
                                i.add_card(card_name)
                else:
                    print("There is no worksheet with this name")
    print("Cards built successfully")

