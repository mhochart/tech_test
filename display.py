"""
Here are the functions for the action analysis display and the generation of the game recreation JSON file.
"""

##################### IMPORTS #####################

import matplotlib.pyplot as plt
import numpy as np
import json
import os

#################### FUNCTIONS ####################

# function for the action analysis results visualization
def display_analysis(dic_actions):
    attributes = ('Duration mean', 'Norm mean', 'Consecutiveness mean') # attributes of each action
    new_dic = {}                                        # init dictionnary: {'shot':(float, float, float), 'pass':(float, float, float), ...} with each tuple for 'Duration mean', 'Norm mean' & 'Consecutiveness mean'
    # browsing actions
    for key in dic_actions:
        values = tuple(dic_actions[key].values())       # tuple creation
        new_dic[key] = values                           # tuple in the dictionnary

    x = np.arange(len(attributes))                      # the label locations
    width = 0.06                                        # the width of the bars
    multiplier = 0                                      # multiplier init

    fig, ax = plt.subplots(layout='constrained')        # creation of the matplotlib window

    # browsing the dictionnary
    for attribute, measurement in new_dic.items():
        offset = width * multiplier                     # offset of the bar
        rects = ax.bar(x + offset, measurement, width, label=attribute) # bar creation
        ax.bar_label(rects, padding=3)                  # adding the bar
        multiplier += 1                                 # shifting the next bar

    # adding some text for labels, title and custom x-axis tick labels
    ax.set_title('Actions analysis')
    ax.set_xticks(x + 4*width, attributes)
    ax.legend(loc='upper left')
    ax.set_ylim(0, 105)

    plt.show()                                          # posting the window

# function for saving the game recreation dictionnary in a JSON file
def save_json(game_dict):
    output_dir = './output/'                            # Define the output directory path
    os.makedirs(output_dir, exist_ok=True)              # Create the output directory if it doesn't exist
    output_file = os.path.join(output_dir, 'game_recreation.json')  # Specify the output file path within the output directory

    with open(output_file, 'w') as outfile:
        json.dump(game_dict, outfile)
