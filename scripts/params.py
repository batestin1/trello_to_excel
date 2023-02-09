import json

def parameters():
    with open('paramenters/paramenters.json') as f:
        data = json.load(f)

    dir_excel = input("Enter the path and name of your excel file: ")
    worksheet = input('Enter the name of the sheet you want to use: ')
    data['dir_excel'] = dir_excel.replace("\\", "/")
    data['worksheet'] = worksheet

    with open('paramenters/paramenters.json', 'w') as f:
        json.dump(data, f, indent=4)
