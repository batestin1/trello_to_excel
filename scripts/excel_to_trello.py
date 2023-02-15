#!/usr/local/bin/python3

###################################################################################################
#                                                                                                 #
# SCRIPT FILE: excel_to_trello.py                                                                 #
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

import requests
import pandas as pd
import json
from optional.del_board import del_boards
import time
from trello_to_excel import to_excel


with open('paramenters/keys.json') as f:
    keys = json.load(f)

with open('paramenters/paramenters.json') as f:
    parameters = json.load(f)

yourKey = keys['yourKey']
yourToken = keys['yourToken']
url_board = parameters['url_board']
url_base = parameters['url_base']
dir = parameters["dir_excel"]
field_get_id = parameters['field_get_id']
methods = parameters['methods']
worksheet = parameters['worksheet']
prefs_background = parameters['prefs_background']

board_id = None
card_title = "Practitioner Notes ID"

df = pd.read_excel(dir, sheet_name=None)

def get_custom_field_id(board_id, field_name):
    url_get = f"{url_base}boards/{board_id}/customFields"
    headers_get = {"Accept": "application/json"}
    query = {'key':yourKey,'token':yourToken}
    response = requests.request(methods[0],url_get,headers=headers_get,params=query).json()
    for field in response:
        if field['name'] == field_name:
            return field['id']

def update_field():
    global board_id, card_title
    url = f"{url_base}boards/{board_id}/cards?key={yourKey}&token={yourToken}"
    response = requests.get(url).json()
    for card in response:
        if card_title in card['name']:
            for col in df[worksheet].columns:
                if col != card_title:
                    field_name = col
                    field_id = get_custom_field_id(board_id, field_name)
                    if field_id:
                        values = {
                            "value": {
                                "text": f"{df[worksheet][df[worksheet][card_title] == card['name']][col].values[0]}"
                            }
                        }
                        url_field = f"{url_base}cards/{card['id']}/customField/{field_id}/item?key={yourKey}&token={yourToken}"
                        requests.put(url_field, json=values)
                    else:
                        print(f"custom field '{field_name}' not found")

def create_board():
    global board_id
    if worksheet not in df:
        print(f"There is no worksheet with the name {worksheet}")
        return

    # check if the board already exists on Trello
    url = f"{url_base}{field_get_id}&key={yourKey}&token={yourToken}"
    response = requests.get(url).json()
    names = [item['name'] for item in response]
    if worksheet in names:
        print(f"The board {worksheet} already exists!")
        choice = input("Do you want to update the information?[Y/N] ")[0].lower()
        if choice == 'y':
            print("Doing some backup")
            to_excel()
            time.sleep(1)
            del_boards()
            time.sleep(1)
            print("update the board with new informations")
            create_new_board()
    else:
        # create a new board
        create_new_board()

def create_new_board():
    global board_id, card_title
    # create a new board on Trello
    payload = {
        "name": f"{worksheet}",
        "defaultLists": False,
        "prefs_cardCovers": False,
        "prefs_background": prefs_background
    }
    query = {"key": yourKey, "token": yourToken}
    response = requests.post(url_board, json=payload, params=query).json()

    # check that the response from the Trello API contains a valid ID for the new board
    if 'id' in response:
        board_id = response["id"]

        # create custom fields for the board on Trello
        df_worksheet = pd.read_excel(dir, sheet_name=worksheet)
        column_names = list(df_worksheet.columns)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        query = {"key": yourKey, "token": yourToken}
        for column_name in column_names:
            url = f"{url_base}/customFields"
            display_card_front = False
            if column_name in ["Availability Date", "Bench Roll off", "Job Role/Specialty", "Band"]:
                display_card_front = True
            payload = {
                "idModel": board_id,
                "name": column_name,
                "type": "text",
                "pos": "bottom",
                "modelType": "board",
                "display_cardFront": display_card_front,
                "isSuggestedField": True
            }
            response = requests.post(url, json=payload, headers=headers, params=query)

        # create lists for each unique value in the "Current Week Action" column
        current_week_actions = list(df_worksheet["Current Week Action"].unique())
        for cwa in current_week_actions:
            # create a new list on Trello with the name of the current week action
            url = f"{url_base}/lists"
            payload = {
                "name": cwa,
                "idBoard": board_id,
                "pos": "bottom"
            }
            response = requests.post(url, json=payload, headers=headers, params=query).json()
            list_id = response["id"]

            # create a new card on Trello for each Practitioner Notes ID associated with the current week action
            practitioner_notes_ids = list(df_worksheet.loc[df_worksheet["Current Week Action"] == cwa, "Practitioner Notes ID"])
            for pni in practitioner_notes_ids:
                url = f"{url_base}/cards"
                payload = {
                    "name": pni,
                    "idList": list_id,
                    "cardCovers": False
                }
                response = requests.post(url, json=payload, headers=headers, params=query).json()
                card_id = response["id"]

                # Create a checklist with the name of the "Comments" column and items for each value in the column
                if "Comments" in column_names:
                    checklist_items = list(df_worksheet.loc[df_worksheet["Practitioner Notes ID"] == pni, "Comments"])
                    if len(checklist_items) > 0:
                        url_checklist = f"{url_base}/checklists"
                        query_checklist = {"key": yourKey, "token": yourToken}
                        headers_checklist = {"Accept": "application/json", "Content-Type": "application/json"}
                        payload_checklist = {
                            "name": "Comments",
                            "idCard": card_id,
                            "pos": "bottom"
                        }
                        response_checklist = requests.post(url_checklist, json=payload_checklist, headers=headers_checklist, params=query_checklist).json()
                        checklist_id = response_checklist["id"]
                        for item in checklist_items:
                            url_item = f"{url_base}/checklists/{checklist_id}/checkItems"
                            query_item = {"key": yourKey, "token": yourToken}
                            headers_item = {"Accept": "application/json", "Content-Type": "application/json"}
                            payload_item = {
                                "name": item,
                                "checked": False
                            }
                            response_item = requests.post(url_item, json=payload_item, headers=headers_item, params=query_item)

                # update custom fields for the card
                df_worksheet = pd.read_excel(dir, sheet_name=worksheet)
                column_names = list(df_worksheet.columns)
                card_title = "Practitioner Notes ID"
                for col in column_names:
                    if col != card_title:
                        field_name = col
                        field_id = get_custom_field_id(board_id, field_name)
                        if field_id:
                            values = {
                                "value": {
                                    "text": f"{df_worksheet[df_worksheet[card_title] == pni][col].values[0]}"
                                }
                            }
                            url_field = f"{url_base}cards/{card_id}/customField/{field_id}/item?key={yourKey}&token={yourToken}"
                            requests.put(url_field, json=values)
                        else:
                            print(f"custom field '{field_name}' not found")

