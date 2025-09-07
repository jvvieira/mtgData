import os
import pandas as pd
import numpy as np

def get_files(directory_path):
    file_paths = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_paths.append(os.path.join(root, file))

    return file_paths

def split_file_topdeck(file_path, delimiter):
    with open(file_path) as f:
        return_data=[]
        should_read=False
        for line in f:
            if line.strip() == delimiter:
                should_read=True
                continue
            elif line.strip().startswith("~~"):
                should_read=False
                continue

            if should_read:
                if len(line.strip()) > 0:
                    original_string = line.strip()
                    postion = original_string.find(" ")
                    return_data.append([original_string[0:postion], original_string[postion:]])
    return return_data

def split_file_moxfield(file_path, delimiter):
    with open(file_path) as f:
        return_data=[]
        should_read=False
        for line in f:
            if line.strip() == delimiter:
                should_read=True
                continue
            elif line.strip().startswith("~~"):
                should_read=False
                continue

            if should_read:
                if len(line.strip()) > 0:
                    original_string = line.strip()
                    insert_string = "$"
                    index = 2

                    new_string = "{}{}{}".format(original_string[:index], insert_string, original_string[index:])
                    return_data.append(new_string.split("$"))
    return return_data

# Get decklists
all_decklists = pd.DataFrame()
all_commanders = pd.DataFrame()

## TopDeck
all_files = get_files("./decklists/topdeck")
print("Total Decks Top Deck: ", len(all_files))

### Decklists
for filename in all_files:
    decklsit = np.array(split_file_topdeck(filename, "~~Mainboard~~"))
    df  = pd.DataFrame(decklsit, columns=["qtd", "card_name"])
    df['decklist'] = filename.split('/')[3]
    df = df.dropna()
    all_decklists = pd.concat([all_decklists, df])

all_decklists['qtd'] = all_decklists['qtd'].astype(int)

### Commanders
for filename in all_files:
    decklsit = np.array(split_file_topdeck(filename, "~~Commanders~~"))
    df  = pd.DataFrame(decklsit, columns=["qtd", "card_name"])
    df['decklist'] = filename.split('/')[3]
    df = df.dropna()
    all_commanders = pd.concat([all_commanders, df])

all_commanders['qtd'] = all_commanders['qtd'].astype(int)

## Moxfield
all_files = get_files("./decklists/moxfield")
print("Total Decks Moxfield: ", len(all_files))

### Decklists

# Get the most used cards
# all_decklists = all_decklists.iloc[:, [0,1]].groupby('card_name').agg('sum')
# print(all_decklists.sort_values(by='qtd', ascending=False))


# Get Comanders
all_commanders = all_commanders.iloc[:, [0,1]].groupby('card_name').agg('sum')
print(all_commanders.sort_values(by='qtd', ascending=False))
# print(all_commanders.sort_values(by='card_name'))