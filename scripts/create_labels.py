#!/usr/local/bin/python3

###################################################################################################
#                                                                                                 #
# SCRIPT FILE: create_labels.py                                                                   #
# CREATION DATE: 02/02/2023                                                                       #
# HOUR: 10:10                                                                                     #
# DISTRIBUTION USED: UBUNTU                                                                       #
# OPERATIONAL SYSTEM: LINUX                                                                       #
#                                                                             DEVELOPED BY: BATES #
###################################################################################################
#                                                                                                 #
# SUMMARY: Creating a lebel to card on trello based on sheets of excel files                      #
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

 # Obtenha o board no qual você deseja adicionar labels
     
boards = client.list_boards()
for board in boards:
    if board.name == worksheet:
        df = pd.read_excel(dir, sheet_name=worksheet)
        a = df.iloc[0].to_dict()
        columns_ = list(a.keys())
        values_ = str(list(a.values())).replace("Timestamp('","").replace("')","").replace("datetime.time(","").replace(")","")
        board = client.get_board(board.id)
        cards = board.get_cards()
        for n in range(len(columns_)):
            if cards[n].name in list(df.iloc[n]):
                id_card = cards[n].id
                card = client.get_card(id_card)
                print(f"{card.name} - {card.id}")
            else:
                pass
''' 
for board in boards:
    if board.name == worksheet:
        df = pd.read_excel(dir, sheet_name=worksheet)
        board = client.get_board(board.id)
        cards = board.get_cards()
        for n in range(len(cards)):
            if cards[n].name in list(df['coluna_desejada'][n]):
                id_card = cards[n].id
                card = client.get_card(id_card)
                card.add_custom_field({'value': str(df['coluna_desejada'][n])})
            else:
                pass

'''