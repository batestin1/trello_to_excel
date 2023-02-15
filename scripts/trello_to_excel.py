#!/usr/local/bin/python3

###################################################################################################
#                                                                                                 #
# SCRIPT FILE: trello_to_excel.py                                                                 #
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

import pandas as pd
import requests
import json
from datetime import datetime
import os

with open('paramenters/keys.json') as f:
    keys = json.load(f)

with open('paramenters/paramenters.json') as f:
    parameters = json.load(f)

yourKey = keys['yourKey']
yourToken = keys['yourToken']
url_board = parameters['url_board']
url_base = parameters['url_base']
worksheet = parameters['worksheet']
prefs_background = parameters['prefs_background']
field_get_id = parameters['field_get_id']
methods = parameters['methods']
dir_backup = parameters['dir_backup']
url_export = parameters['url_export']
field_for_url = parameters['field_for_url']

url_get_board_id = f"{url_base}members/me/boards?key={yourKey}&token={yourToken}&fields=name"
response_board_id = requests.get(url_get_board_id).json()
data_now = datetime.now().strftime("%Y%m%d_%H%M%S")
names = [item['name'] for item in response_board_id]
id_board= response_board_id[0]['id']

url_get_organization = f'{url_board}{id_board}/?&key={yourKey}&token={yourToken}'
response = requests.get(url_get_organization ).json()
id_organization = response['idOrganization']

url_final = f'{url_board}{id_board}/cards?key={yourKey}&token={yourToken}&{field_for_url}'

response = requests.get(url_final)
data = []
count = len(list(response.json()))

def to_excel():
    for i in range(count):
        try:
            comments = response.json()[i]["checklists"][0]["checkItems"][0]["name"]
        except (KeyError, IndexError):
            comments = "nan"

        df = {
            "Practitioner Notes ID": response.json()[i]["name"],
            "Comments": comments,
            "CNUM": response.json()[i]["customFieldItems"][0]['value']['text'],
            "Availability Date": response.json()[i]["customFieldItems"][1]['value']['text'],
            "Extension Date": response.json()[i]["customFieldItems"][2]['value']['text'],
            "Bench Roll off": response.json()[i]["customFieldItems"][3]['value']['text'],
            "BBD" : response.json()[i]["customFieldItems"][4]['value']['text'],
            "CQ" : response.json()[i]["customFieldItems"][5]['value']['text'],
            "Bench Ageing (Days)" : response.json()[i]["customFieldItems"][6]['value']['text'],
            "Approching Bench" : response.json()[i]["customFieldItems"][7]['value']['text'],
            "BBH" : response.json()[i]["customFieldItems"][8]['value']['text'],
            "Reallocation Status": response.json()[i]["customFieldItems"][9]['value']['text'],
            "Status Date": response.json()[i]["customFieldItems"][10]['value']['text'],
            "Open Seat" : response.json()[i]["customFieldItems"][11]['value']['text'],
            "OS Client Name": response.json()[i]["customFieldItems"][12]['value']['text'],
            "OS Start Date" : response.json()[i]["customFieldItems"][13]['value']['text'],
            "Contribution Control" : response.json()[i]["customFieldItems"][14]['value']['text'],
            "Contribution Control Account Group" : response.json()[i]["customFieldItems"][15]['value']['text'],
            "Current Week Action": response.json()[i]["customFieldItems"][16]['value']['text'],
            "New Project / Assignment" : response.json()[i]["customFieldItems"][18]['value']['text'],
            "Planned start date": response.json()[i]["customFieldItems"][19]['value']['text'],
            "Job Role/Specialty": response.json()[i]["customFieldItems"][20]['value']['text'],
            "Geography": response.json()[i]["customFieldItems"][21]['value']['text'],
            "Market Region": response.json()[i]["customFieldItems"][22]['value']['text'],
            "Country": response.json()[i]["customFieldItems"][23]['value']['text'],
            "EMF Status": response.json()[i]["customFieldItems"][24]['value']['text'],
            "Band": response.json()[i]["customFieldItems"][25]['value']['text'],
            "Billable":response.json()[i]["customFieldItems"][26]['value']['text'],
            "Exists in PPA": response.json()[i]["customFieldItems"][27]['value']['text'],
            "Manager Notes ID": response.json()[i]["customFieldItems"][28]['value']['text'],
            "JR/S Growth Platform": response.json()[i]["customFieldItems"][29]['value']['text'],
            "JR/S Service Line" :response.json()[i]["customFieldItems"][30]['value']['text'],
            "JR/S Practice": response.json()[i]["customFieldItems"][31]['value']['text'],
            "RSP Notes ID": response.json()[i]["customFieldItems"][32]['value']['text'],
            "Resource Work City" :response.json()[i]["customFieldItems"][33]['value']['text'],
            "Last CV Update": response.json()[i]["customFieldItems"][34]['value']['text'],
            "Secondary JR/S": response.json()[i]["customFieldItems"][35]['value']['text'],
            "Languages" : response.json()[i]["customFieldItems"][36]['value']['text'],
            "+60 Bench": response.json()[i]["customFieldItems"][37]['value']['text']

        }
        data.append(df)

    df = pd.DataFrame(data)
    file_name = f"dt_backup_{data_now}.xlsx"
    file_path = os.path.join(dir_backup, file_name)

    if os.path.exists(file_path):
        os.remove(file_path)

    if not os.path.exists(dir_backup):
        os.makedirs(dir_backup)

    with pd.ExcelWriter(file_path) as writer:
        df.to_excel(writer, sheet_name=worksheet, index=False)
    return print(f"Your data is save on {file_path} with the name {file_name}")
