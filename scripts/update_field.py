#!/usr/local/bin/python3

###################################################################################################
#                                                                                                 #
# SCRIPT FILE: update_field.py                                                                    #
# CREATION DATE: 02/02/2023                                                                       #
# HOUR: 10:10                                                                                     #
# DISTRIBUTION USED: UBUNTU                                                                       #
# OPERATIONAL SYSTEM: LINUX                                                                       #
#                                                                             DEVELOPED BY: BATES #
###################################################################################################
#                                                                                                 #
# SUMMARY: Updating a field on trello based on sheets of excel files                              #
#                                                                                                 #
###################################################################################################

# imports
import pandas as pd
from trello import TrelloClient
import json
import requests

parKeys = open('paramenters/keys.json')
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
list_title = content_parm['list']
card_title = content_parm['card']

client = TrelloClient(
    api_key=yourKey,
    token=yourToken
)

boards = client.list_boards()

def get_custom_field_id(board_id, field_name):
    url_get = f"{url_base}boards/{board_id}/customFields"
    headers_get = {"Accept": "application/json"}
    query = {'key':yourKey,'token':yourToken}
    response = requests.request(methods[0],url_get,headers=headers_get,params=query).json()
    for field in response:
        if field['name'] == field_name:
            return field['id']

def update_field():
    for board in boards:
        if board.name == worksheet:
            a = client.get_board(board.id)
            df = pd.read_excel(dir, sheet_name=worksheet)
            check_name = df[card_title].to_dict()
            check_name = list(check_name.values())
            for i in a.open_cards():
                if i.name in check_name:
                    for col in df.columns:
                        if col != card_title:
                            field_name = col
                            field_id = get_custom_field_id(board.id, field_name)
                            if field_id:
                                values = {
                                    "value": {
                                        "text": f"{df[df[card_title] == i.name][col].values[0]}"
                                    }
                                }
                                url_field = f"{url_base}cards/{i.id}/customField/{field_id}/item?key={yourKey}&token={yourToken}"
                                requests.put(url_field, json=values)
                            else:
                                print(f"custom field '{field_name}' not found")
                else:
                    print(f"Board '{i.name}' not found")

if __name__ == "__main__":
    update_field()