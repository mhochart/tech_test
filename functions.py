"""
Here are the functions for the action analysis and game recreation.
"""

##################### IMPORTS #####################

from statistics import mean

#################### FUNCTIONS ####################

# function for the action analysis
def action_analysis(list_players):
    dic_actions = {}                                # init dict: {'walk': {'length': float, 'average': float, 'consecutiveness': float}, 'rest': {'length': float, 'average': float, 'consecutiveness': float}, ...}

    list_time = []                                  # list of time steps
    # browsing players
    for player_dict in list_players:
        time = 0                                    # init time at 0
        list_gaits = list(player_dict.values())[0]  # list of a player's gaits

        already_label = []                          # a list of the labels
        previous_label = ''                         # init the previous label when browsing
        consecutiveness = 0                         # init label consecutiveness

        # browsing gaits
        for gait in list_gaits:
            label = gait['label']                   # label gathering
            list_norms = gait['norm']               # norms list gathering
            length_norms = len(list_norms)          # norms list length
            norm_avg = mean(list_norms)             # mean of the norms list

            time += length_norms/50                 # gait end indentation

            if label == previous_label:             # 2 gaits with the same label
                consecutiveness += 1
            else:                                   # 2 gaits with different labels
                consecutiveness = 0

            if label in already_label:              # the label is already in dic_actions
                dic_actions[label]['list_length'].append(length_norms)  # gait duration -> dic_actions
                dic_actions[label]['list_avg'].append(norm_avg) # norm mean -> dic_actions
                dic_actions[label]['list_consecutiveness'].append(consecutiveness)  # consecutiveness -> dic_actions
            else:                                   # the label is not in dic_actions yet
                dic_actions[label] = {'list_length':[length_norms], 'list_avg':[norm_avg], 'list_consecutiveness':[consecutiveness]}    # init dic_actions[label]
            already_label.append(label)             # adding the label in the already_label list
            previous_label = label                  # the label becomes previous_label for the next gait
        list_time.append(time)                      # time step added in list_time

    # browsing actions
    for action in dic_actions:
        avg_len = mean(dic_actions[action]['list_length'])  # mean of the gait durations
        dic_actions[action].pop('list_length', None)    # pop durations list from dic_actions
        dic_actions[action]['length'] = avg_len/50  # adding the mean (in seconds) to dic_actions

        avg = mean(dic_actions[action]['list_avg']) # mean of the norms list
        dic_actions[action].pop('list_avg', None)   # pop norms list form dic_actions
        dic_actions[action]['average'] = avg        # adding the norms mean to dic_actions

        pre_avg_cons = []                           # init an intermediate list

        # when the consecutiveness is not 0, there is a sequel 0, 1, 2, ... until the highest value
        # here we only keep the highest value when there is such a sequel
        for i in range(len(dic_actions[action]['list_consecutiveness']) -1):
            if not dic_actions[action]['list_consecutiveness'][i] < dic_actions[action]['list_consecutiveness'][i+1]:
                pre_avg_cons.append(dic_actions[action]['list_consecutiveness'][i])
        pre_avg_cons.append(dic_actions[action]['list_consecutiveness'][-1])

        avg_cons = mean(pre_avg_cons)               # mean of the consecutivenesses
        dic_actions[action].pop('list_consecutiveness', None)   # pop consecutivenesses list from dic_actions
        dic_actions[action]['consecutiveness'] = avg_cons   # adding the consecutivenesses mean to dic_actions
    return dic_actions

# function for the game recreation
def match_recreation(list_by_ts):
    game_list = []                                  # init list of dictionnaries
    game_dict = {}                                  # game recreation dict: {action:[norms], action:[norms], ...}
    attack = ['dribble', 'shot', 'pass', 'cross']   # attack actions list
    no_ball = ['rest', 'walk', 'run', 'no action']  # list of actions without the ball
    # browsing time steps
    for timestep in list_by_ts:
        time = timestep['time']                     # time gathering
        attack_list = []                            # list of attacking dict (one element for one player)
        defense_list = {}                           # defense (when the player tackles) dict
        no_ball_list = []                           # list of no ball dict (one element for one player)
        # browsing the timestep keys
        for key in timestep:
            if 'player' in key:                     # excluding the 'time' key
                if timestep[key]['label'] in attack:    # case attack action
                    attack_list.append({'player':key[6] ,'label':timestep[key]['label'], 'norm':timestep[key]['norm']}) # adding the dict to attack_list
        if len(attack_list)==1:                     # only one player is attacking
            game_list.append({'time':time, 'player':attack_list[0]['player'], 'label':attack_list[0]['label'], 'norm':attack_list[0]['norm']})  # the attack action is added to game_list
        elif len(attack_list)==0:                   # no player is attacking
            # browsing the timestep keys
            for key in timestep:
                if 'player' in key:                 # excluding the 'time' key
                    if timestep[key]['label']=='tackle':    # a player is tackling
                        defense_list = {'player':key[6], 'label':timestep[key]['label'], 'norm':timestep[key]['norm']}  # dict -> defense list
                    else:                           # no player is challenging the ball
                        no_ball_list.append({'player':key[6], 'label':timestep[key]['label'], 'norm':timestep[key]['norm']})    # adding the dict to no_ball_list
            if defense_list!={}:                    # a player is tackling
                game_list.append({'time':time, 'player':defense_list['player'], 'label':defense_list['label'], 'norm':defense_list['norm']})    # the tackle action is added to game_list
            else:                                   # no player is challenging the ball
                max_norm = 0                        # init the norm maximum
                max_label = ''                      # init the corresponding label
                max_player = 0                      # init the corresponding player number
                # browsing the actions in no_ball_list
                for no_ball_action in no_ball_list:
                    if no_ball_action['norm'] >= max_norm:  # we choose the label with the highest norm
                        max_label, max_norm, max_player = no_ball_action['label'], no_ball_action['norm'], no_ball_action['player'] # updating maximums
                game_list.append({'time':time, 'player':max_player, 'label':max_label, 'norm':max_norm})    # adding the action with the highest norm to game_list
        elif len(attack_list)>1:                    # more than one player are attacking
            max_norm_attack = 0                     # init the norm maximum
            max_label_attack = ''                   # init the corresponding label
            max_player_attack = 0                   # init the corresponding player number
            # browsing the attack actions
            for attack_action in attack_list:
                if attack_list[0]['norm']>=max_norm_attack: # we choose the label with the highest norm
                    max_label_attack, max_norm_attack, max_player_attack = attack_list[0]['label'], attack_list[0]['norm'], attack_list[0]['player']    # updating maximums
            game_list.append({'time':time, 'player':max_player_attack, 'label':max_label_attack, 'norm':max_norm_attack})   # adding the action with the highest norm to game_list

    # we will regroup timesteps in gaits following several conditions:
    #   - the same player is doing the same action
    #   - from one player doing an action without the ball to another player doing the same action
    list_labels = [game_list[0]['label']]           # init the labels list
    list_norms = []                                 # init a list of list1gait
    list1gait = [game_list[0]['norm']]              # init the norms list for 1 gait
    # browsing game_list
    for i in range(1, len(game_list)):
        if game_list[i]['player']==game_list[i-1]['player'] and game_list[i]['label']==game_list[i-1]['label']: # the same player is doing the same action
            list1gait.append(game_list[i]['norm'])  # adding the norms to list1gait
        elif game_list[i]['label'] in no_ball and game_list[i-1]['label'] in no_ball and game_list[i]['label']==game_list[i-1]['label']:    # from one player doing an action without the ball to another player doing the same action
            list1gait.append(game_list[i]['norm'])  # adding the norms to list1gait
        else:                                       # new gait
            list_norms.append(list1gait)            # the gait norms added to list_norms
            list_labels.append(game_list[i]['label'])   # new label added to list_labels
            list1gait = [game_list[i]['norm']]      # updating list1gait
    list_norms.append(list1gait)                    # adding the last list1gait to list_norms
    # creation of the game recreation dictionnary
    for i in range(len(list_labels)):
        game_dict[list_labels[i]] = list_norms[i]

    # exceptions management: we make sure each action except rest & no action is longer than 0.2 s and shorter than 2 s
    corr_game_dict = {}                             # init a corrected dictionnary
    # browsing actions
    for key in game_dict:
        if key not in ['no action', 'rest'] and (len(game_dict[key])<0.2*50 or len(game_dict[key])>2*50):   # in this case the action is not logical
            corr_game_dict['no action'] = None      # we replace the illogical action by 'no action'
        else:                                       # logical action
            corr_game_dict[key] = game_dict[key]    # added to the corrected dictionnary
    return corr_game_dict
