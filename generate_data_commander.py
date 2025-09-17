import os
import pandas as pd
import numpy as np

### Treshhold for cards appearence
rate = 0.1

### Card to investigate
card_name = 'Food Chain'



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
                    return_data.append([original_string[0:postion].strip(), original_string[postion:].strip()])
    return return_data

def split_file_moxfield(file_path, delimiter):
    with open(file_path) as f:
        return_data=[]
        should_read=False

        for line in f:
            if delimiter == "~~Mainboard~~":
                 should_read=True
            if delimiter == "~~Mainboard~~" and len(line.strip()) == 0:
                 break
            
            if delimiter == "~~Commanders~~" and len(line.strip()) == 0:
                should_read=True
                continue

            if should_read:
                if len(line.strip()) > 0:
                    original_string = line.strip()
                    postion = original_string.find(" ")
                    return_data.append([original_string[0:postion].strip(), original_string[postion:].strip()])
    return return_data

# Get decklists
all_decklists = pd.DataFrame()
all_commanders = pd.DataFrame()
total_decklists = 0

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

### Commanders
for filename in all_files:
    decklsit = np.array(split_file_topdeck(filename, "~~Commanders~~"))
    df  = pd.DataFrame(decklsit, columns=["qtd", "card_name"])
    df['decklist'] = filename.split('/')[3]
    df = df.dropna()
    all_commanders = pd.concat([all_commanders, df])

total_decklists += len(all_files)

## Moxfield
all_files = get_files("./decklists/moxfield")
print("Total Decks Moxfield: ", len(all_files))

## Decklists
for filename in all_files:
    decklsit = np.array(split_file_moxfield(filename, "~~Mainboard~~"))
    df  = pd.DataFrame(decklsit, columns=["qtd", "card_name"])
    df['decklist'] = filename.split('/')[3]
    df = df.dropna()
    all_decklists = pd.concat([all_decklists, df])


### Commanders
for filename in all_files:
    decklsit = np.array(split_file_moxfield(filename, "~~Commanders~~"))
    df  = pd.DataFrame(decklsit, columns=["qtd", "card_name"])
    df['decklist'] = filename.split('/')[3]
    df = df.dropna()
    all_commanders = pd.concat([all_commanders, df])


total_decklists += len(all_files)

print("Total de cards: ", len(all_decklists))


# Get Comanders
all_commanders["qtd"] = all_commanders["qtd"].astype(int)
all_commanders["card_name"] = all_commanders["card_name"].str.strip()
df_aggr = all_commanders.iloc[:, [0,1]].groupby('card_name').agg('sum')
# print(df_aggr.sort_values(by='qtd', ascending=False))

# Get the most used cards
all_decklists["qtd"] = all_decklists["qtd"].astype(int)
all_decklists["card_name"] = all_decklists["card_name"].str.strip()

## remove basic lands
basic_lands = ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']
all_decklists = all_decklists[~all_decklists['card_name'].isin(basic_lands)]

df_aggr = all_decklists.iloc[:, [0,1]].groupby('card_name').agg('sum')
print("Cards Similares: ", len(df_aggr[df_aggr['qtd']>= total_decklists * rate]))
#print(df_aggr.sort_values(by='qtd', ascending=False)[df_aggr['qtd'] >= total_decklists * rate])


# Card Search
# df_decklists = all_decklists[all_decklists['card_name'] == card_name]
# df_commanders = all_commanders[all_commanders['decklist'].isin(df_decklists['decklist'].tolist())]

# print(df_commanders.sort_values(by='card_name'))