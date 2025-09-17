import os
import pandas as pd
import numpy as np


def get_files(directory_path):
    file_paths = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_paths.append(os.path.join(root, file))

    return file_paths

def split_file_pauper(file_path):
    with open(file_path) as f:
        return_data=[]
        is_mainboard = True

        for line in f:
            if len(line.strip()) == 0 or line.strip() == 'Sideboard':
                is_mainboard = False
                continue
            
            original_string = line.strip()
            postion = original_string.find(" ")
            return_data.append([original_string[0:postion].strip(), original_string[postion:].strip(), is_mainboard])
    return return_data


all_files = get_files("./decklists/pauper")
all_decklists = pd.DataFrame()


### Get Decklists
for filename in all_files:
    decklsit = np.array(split_file_pauper(filename))
    df  = pd.DataFrame(decklsit, columns=["qtd", "card_name", "mainboard"])
    df['decklist'] = filename.split('/')[3]
    df = df.dropna()
    all_decklists = pd.concat([all_decklists, df])

unique_cards = all_decklists['card_name'].unique()

print(len(unique_cards))
