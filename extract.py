"""
Here is the pre-processing function to extract the data in a convenient form.
"""

##################### IMPORTS #####################

import json
import os

##################### FUNCTION #####################

def extract_list_players_dict():
    current_directory = os.getcwd()             # get the current directory
    files = os.listdir(current_directory)       # list all files in the current directory
    json_files = [file for file in files if file.startswith('match_') and file.endswith('.json')]  # filter JSON files and load them into dictionaries
    list_players = []                           # init list_players: [{'dict_player_1':[{'label': str, 'norm':[floats]}, {'label': str, 'norm':[floats]}, ...]}, {'dict_player_2':[{'label': str, 'norm':[floats]}, {'label': str, 'norm':[floats]}, ...]}, ...]

    nb_players = 0                              # init number of players

    # load JSON files into dictionaries
    for json_file in json_files:
        loaded_data = {}                        # dictionary storing loaded JSON data
        file_number = int(json_file.split('_')[1].split('.')[0]) # extract the integer 'x' from the file name
        # open and load the JSON file into a dictionary
        with open(json_file, 'r') as file:
            loaded_data[f'dict_player_{file_number}'] = json.load(file)
        list_players.append(loaded_data)        # adding the dictionnary in the list
        nb_players += 1                         # +1 player

    list_by_ts = []                             # init list by time step
    dic_players_ts = {}                         # init dict by time step

    h = 0                                       # init the player number
    # browsing players
    for player_dict in list_players:
        tss, actions, norms = [], [], []        # init lists of time steps, labels & norms
        ts = 0                                  # init time step at 0
        gaits = list(player_dict.values())[0]   # gaits list
        # browsing gaits
        for gait in gaits:
            # browsing norms in the same gait
            for norm in gait['norm']:
                actions.append(gait['label'])   # label added in actions list
                norms.append(norm)              # norm added in norms list
                tss.append(ts)                  # time step added in tss list
                ts += 1/50                      # time step indentation (in seconds)
        dic_players_ts[h] = [tss, actions, norms]   # dict[player number] -> [tss, actions, norms]
        h+=1                                    # player number indentation

    min_ts = min(len(dic_players_ts[x][0]) for x in dic_players_ts) # looking for the player with shorter data
    # stop when a player's tracker is not recording anymore
    for i in range(min_ts):
        time = dic_players_ts[0][0][i]          # gathering the time step
        dic_ts = {'time': time}                 # init dic_ts with the time step
        # browsing players
        for j in range(nb_players):
            label = dic_players_ts[j][1][i]     # gathering the label
            norm = dic_players_ts[j][2][i]      # gathering the norm
            dic_ts[f'player{j+1}'] = {'label': label, 'norm': norm} # dict['playerx'] -> {'label': label, 'norm': norm}
        list_by_ts.append(dic_ts)               # dic_ts added in list_by_ts

    return list_players, list_by_ts


