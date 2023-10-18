"""
This is the main code to execute for the actions analysis and the game recreation.
"""

##################### IMPORTS #####################

from extract import extract_list_players_dict
from functions import action_analysis, match_recreation
from display import display_analysis, save_json

#################### MAIN CODE ####################

list_players, list_by_ts = extract_list_players_dict()  # extracting the data in a convenient form

dic_actions = action_analysis(list_players)             # analyzing the actions
display_analysis(dic_actions)                           # visualizing the action analysis

game_dict = match_recreation(list_by_ts)                # recreating the game
save_json(game_dict)                                    # saving the game recreated in a json file
