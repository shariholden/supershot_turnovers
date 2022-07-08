import json
from matplotlib import pyplot as plt
import numpy as np


def dictionary_creator(key_list):
    dictt = {}
    for k in key_list:
        dictt[k] = []
    return dictt


def ss_turnover(filename, dict1, dict2):
    f = open(filename)
    datastore = json.load(f)
    scoreflow = datastore['matchStats']['scoreFlow']['score']
    teams = datastore['matchStats']['teamInfo']['team']
    team1id = teams[0]['squadId']
    team1name = teams[0]['squadName']
    if datastore['matchStats']['teamStats']['team'][0]['squadId'] == team1id:
        team1supershots = datastore['matchStats']['teamStats']['team'][0]['goal_from_zone2']
        team2supershots = datastore['matchStats']['teamStats']['team'][1]['goal_from_zone2']
    else:
        team1supershots = datastore['matchStats']['teamStats']['team'][1]['goal_from_zone2']
        team2supershots = datastore['matchStats']['teamStats']['team'][0]['goal_from_zone2']
    team2id = teams[1]['squadId']
    team2name = teams[1]['squadName']
    team1turnover, team2turnover = 0, 0
    for k in range(len(scoreflow)):
        if scoreflow[k]['scoreName'] == "2pt Miss":
            if k + 1 != len(scoreflow) and scoreflow[k + 1]['period'] == scoreflow[k]['period']:
                if scoreflow[k]['squadId'] == team1id and scoreflow[k + 1]['squadId'] == team2id:
                    team1turnover += 1
                elif scoreflow[k]['squadId'] == team2id and scoreflow[k + 1]['squadId'] == team1id:
                    team2turnover += 1
    try:
        team1ratio = team1supershots / (team1turnover + team1supershots)
    except ZeroDivisionError:
        team1ratio = np.nan
    try:
        team2ratio = team2supershots / (team2turnover + team2supershots)
    except ZeroDivisionError:
        team2ratio = np.nan

    # create dictionary
    dict1[team1name].append(team1ratio)
    dict1[team2name].append(team2ratio)
    dict2[team1name].append(team2ratio)
    dict2[team2name].append(team1ratio)

    return dict1, dict2


if __name__ == '__main__':
    team_list = ['Adelaide Thunderbirds', 'Collingwood Magpies', 'GIANTS Netball', 'Melbourne Vixens', 'NSW Swifts',
                 'Queensland Firebirds', 'Sunshine Coast Lightning', 'West Coast Fever']
    ratio_for, ratio_against = dictionary_creator(team_list), dictionary_creator(team_list)
    for i in range(1, 10):
        for j in range(1, 5):
            ratio_for, ratio_against = ss_turnover('116650' + str(i) + '0' + str(j) + '.json', ratio_for, ratio_against)
    for i in range(10, 15):
        for j in range(1, 5):
            ratio_for, ratio_against = ss_turnover('11665' + str(i) + '0' + str(j) + '.json', ratio_for, ratio_against)
    print(ratio_for, ratio_against)

    x = list(range(1, 15))

    ax = plt.axes()
    ax.set_facecolor('cornsilk')
    plt.title('Supershots scored vs turnovers from supershot attempts for each team per round')
    plt.ylabel('Supershots scored vs turnovers from supershot attempts')
    plt.xlabel('Round')
    plt.plot(x, ratio_for['Adelaide Thunderbirds'], label='Adelaide Thunderbirds', color='hotpink')
    plt.plot(x, ratio_for['Collingwood Magpies'], label='Collingwood Magpies', color='gray')
    plt.plot(x, ratio_for['GIANTS Netball'], label='GIANTS Netball', color='darkorange')
    plt.plot(x, ratio_for['Melbourne Vixens'], label='Melbourne Vixens', color='navy')
    plt.plot(x, ratio_for['NSW Swifts'], label='NSW Swifts', color='red')
    plt.plot(x, ratio_for['Queensland Firebirds'], label='Queensland Firebirds', color='purple')
    plt.plot(x, ratio_for['Sunshine Coast Lightning'], label='Sunshine Coast Lightning', color='gold')
    plt.plot(x, ratio_for['West Coast Fever'], label='West Coast Fever', color='limegreen')
    plt.plot(x, [0.5] * 14, color='lightgrey', linestyle='dashed')
    plt.grid()
    plt.legend()
    plt.show()

    ax = plt.axes()
    ax.set_facecolor('cornsilk')
    plt.title('Supershots scored vs turnovers from supershot attempts against each team per round')
    plt.ylabel('Supershots scored vs turnovers from supershot attempts')
    plt.xlabel('Round')
    plt.plot(x, ratio_against['Adelaide Thunderbirds'], label='Adelaide Thunderbirds', color='hotpink')
    plt.plot(x, ratio_against['Collingwood Magpies'], label='Collingwood Magpies', color='gray')
    plt.plot(x, ratio_against['GIANTS Netball'], label='GIANTS Netball', color='darkorange')
    plt.plot(x, ratio_against['Melbourne Vixens'], label='Melbourne Vixens', color='navy')
    plt.plot(x, ratio_against['NSW Swifts'], label='NSW Swifts', color='red')
    plt.plot(x, ratio_against['Queensland Firebirds'], label='Queensland Firebirds', color='purple')
    plt.plot(x, ratio_against['Sunshine Coast Lightning'], label='Sunshine Coast Lightning', color='gold')
    plt.plot(x, ratio_against['West Coast Fever'], label='West Coast Fever', color='limegreen')
    plt.plot(x, [0.5] * 14, color='lightgrey', linestyle='dashed')
    plt.grid()
    plt.legend()
    plt.show()

    new_dict_for, new_dict_against = {}, {}
    for i in team_list:
        new_dict_for[i] = np.nanmean(ratio_for[i])
        new_dict_against[i] = np.nanmean(ratio_against[i])
    average_for = 0
    for i in team_list:
        average_for += new_dict_for[i]

    ax = plt.axes()
    ax.set_facecolor('cornsilk')
    plt.grid()
    plt.title('Supershots scored vs turnovers from supershot attempts for each team')
    plt.ylabel('Supershots scored vs turnovers from supershot attempts')
    plt.xlabel('Teams')
    plt.bar('Adelaide\nThunderbirds', new_dict_for['Adelaide Thunderbirds'], color='hotpink')
    plt.bar('Collingwood\nMagpies', new_dict_for['Collingwood Magpies'], color='gray')
    plt.bar('GIANTS\nNetball', new_dict_for['GIANTS Netball'], color='darkorange')
    plt.bar('Melbourne\nVixens', new_dict_for['Melbourne Vixens'], color='navy')
    plt.bar('NSW\nSwifts', new_dict_for['NSW Swifts'], color='red')
    plt.bar('Queensland\nFirebirds', new_dict_for['Queensland Firebirds'], color='purple')
    plt.bar('Sunshine Coast\nLightning', new_dict_for['Sunshine Coast Lightning'], color='gold')
    plt.bar('West Coast\nFever', new_dict_for['West Coast Fever'], color='limegreen')
    plt.plot(list(range(-1, 9)), [average_for / 8] * 10, color='lightgrey', linestyle='dashed',
             label='Average supershots scored vs turnovers from supershot attempts')
    plt.legend()
    plt.show()

    ax = plt.axes()
    ax.set_facecolor('cornsilk')
    plt.grid()
    plt.title('Supershots scored vs turnovers from supershot attempts against each team')
    plt.ylabel('Supershots scored vs turnovers from supershot attempts')
    plt.xlabel('Teams')
    plt.bar('Adelaide\nThunderbirds', new_dict_against['Adelaide Thunderbirds'], color='hotpink')
    plt.bar('Collingwood\nMagpies', new_dict_against['Collingwood Magpies'], color='gray')
    plt.bar('GIANTS\nNetball', new_dict_against['GIANTS Netball'], color='darkorange')
    plt.bar('Melbourne\nVixens', new_dict_against['Melbourne Vixens'], color='navy')
    plt.bar('NSW\nSwifts', new_dict_against['NSW Swifts'], color='red')
    plt.bar('Queensland\nFirebirds', new_dict_against['Queensland Firebirds'], color='purple')
    plt.bar('Sunshine Coast\nLightning', new_dict_against['Sunshine Coast Lightning'], color='gold')
    plt.bar('West Coast\nFever', new_dict_against['West Coast Fever'], color='limegreen')
    plt.plot(list(range(-1, 9)), [average_for / 8] * 10, color='lightgrey', linestyle='dashed',
             label='Average supershots scored vs turnovers from supershot attempts')
    plt.legend()
    plt.show()
