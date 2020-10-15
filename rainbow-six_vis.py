import streamlit as st
import pandas as pd
from urllib.request import Request, urlopen
import json
import plotly.graph_objs as go
# from plotly.offline import plot
import awoc
import pickle
import os
from PIL import Image
import numpy as np

def plot_operator(name):
    if 'operator_details.pkl' not in os.listdir('Pickle files'):
        print('Details File not available')
        data = pd.read_csv('Datasets/operators.csv')
        operator_details = {}
        for operator in operators_list:
            if operator.split('-')[1] != 'RESERVE':
                special = input('Enter operator special ability paragraph for ' + operator + ': ')
                bio = input('Enter operator bio:')
                speed = list(data[data['Name'] == operator.split('-')[1]]['Speed'])[0]
                armor = list(data[data['Name'] == operator.split('-')[1]]['Armor'])[0]
                difficulty = list(data[data['Name'] == operator.split('-')[1]]['Difficulty'])[0]
                operator_details[operator] = {'special': special, 'bio': bio, 'speed': speed, 
                                              'armor': armor, 'difficulty': difficulty}
        file = open('Pickle files/operator_details.pkl', 'wb')
        pickle.dump(operator_details, file)
        file.close()
    
    file = open('Pickle files/operator_details.pkl', 'rb')
    operator_details = pickle.load(file)
    file.close()
    print('Details File loaded')
    print(name)
    if name.split('-')[1] != 'RESERVE':
        special_details = operator_details[name]['special']
        bio = operator_details[name]['bio']
        speed = operator_details[name]['speed']
        armor = operator_details[name]['armor']
        difficulty = operator_details[name]['difficulty']
        operator_image = np.asarray(Image.open('Operator details/' + name + ' operator.png'))
        operator_loadout = np.asarray(Image.open('Operator details/' + name + ' loadout.png').resize((900, 500)))
        st.markdown('Operator image'.upper())
        st.image(operator_image)
        st.markdown('Operator loadout'.upper())
        st.image(operator_loadout)
        st.markdown('Operator speed'.upper() + ': ' + str(speed) + "/3")
        st.markdown('Operator armor'.upper() + ': ' + str(armor) + "/3")
        st.markdown('Operator difficulty'.upper() + ': ' + str(difficulty) + "/3")
        st.markdown('Operator special power'.upper())
        st.markdown(special_details)
        st.markdown('Operator bio'.upper())
        st.markdown(bio)
        
    if 'weapon_win_rate_' + name + '.pkl' not in os.listdir('Pickle files'):
        data = pd.read_csv('Datasets/datadump_s5_summary_operator_loadout.csv')
        names = data[data['operator'] == name]
        wins = names[names['nbwins'] > 0]
        total_wins = []
        primary_win_weapons = list(wins['primaryweapon'].unique())
        for weapon in primary_win_weapons:
            weapon_frame = wins[wins['primaryweapon'] == weapon]
            total_wins.append(weapon_frame['nbwins'].sum())
        weapon_win_dict = {'weapon_list': primary_win_weapons, 'total_wins': total_wins}
        file = open('Pickle files/weapon_win_rate_' + name + '.pkl', 'wb')
        pickle.dump(weapon_win_dict, file)
        file.close()
    file =open('Pickle files/weapon_win_rate_' + name + '.pkl', 'rb')
    weapon_win_dict = pickle.load(file)
    file.close()
    
    weapon_data = weapon_win_dict['total_wins']
    weapon_labels = weapon_win_dict['weapon_list']
    pie_weapon = go.Figure(data = [go.Pie(labels = weapon_labels, values = weapon_data)])
    st.markdown('Weapon win rate for '.upper() + name.upper())
    st.plotly_chart(pie_weapon)
        
    if 'operator_data_' + name + '.pkl' not in os.listdir('Pickle files'):
        print('Operator data File not available')
        data = pd.read_csv('Datasets/datadump_s5_summary_operator_loadout.csv')
        names = data[data['operator']==name]
        mean_wins = names['nbwins'].mean()
        mean_kills = names['nbkills'].mean()
        mean_deaths = names['nbdeaths'].mean()
        mean_picks = names['nbpicks'].mean()
        primary_weapons = names['primaryweapon'].value_counts()
        most_picked_primary_weapon = primary_weapons.index[primary_weapons.argmax()]
        secondary_weapons = names['secondaryweapon'].value_counts()
        most_picked_secondary_weapon = secondary_weapons.index[secondary_weapons.argmax()]
        ranks = names['skillrank'].value_counts()
        most_picked_by_rank = ranks.index[ranks.argmax()]
        secondary_gadget = names['secondarygadget'].value_counts()
        most_picked_secondary_gadget = secondary_gadget.index[secondary_gadget.argmax()]
        side = list(names['role'])[0]
        operator_dictionary = {'mean_kills': round(mean_kills, 3), 'mean_deaths':round(mean_deaths, 3), 
                               'mean_wins': round(mean_wins, 3),
                                     'mean_picks':round(mean_picks, 3), 'most_picked_primary_weapon':most_picked_primary_weapon,
                                     'most_picked_secondary_weapon':most_picked_secondary_weapon,
                                     'most_picked_secondary_gadget':most_picked_secondary_gadget.split()[0], 
                                     'most_picked_by_rank':most_picked_by_rank, 'side':side}
        pickle_file = open('Pickle files/operator_data_' + name + '.pkl', "ab")
        pickle.dump(operator_dictionary, pickle_file)
        pickle_file.close()
        
    operator_file = open('Pickle files/operator_data_' + name + '.pkl', "rb")
    operator_dictionary = pickle.load(operator_file)
    operator_file.close()
    print('Operator data File loaded')
    
    operator_details = pd.DataFrame(list(operator_dictionary.values()), 
                                         columns = ['Details'], 
                                         index = ['Mean kills', 'Mean deaths', 'Mean wins', 
                                                  'Mean picks','Top primary weapon', 'Top secondary weapon',
                                                  'Top secondary gadget', 'Most picked by rank', 
                                                  'Attacker/Defender'])
    
    st.sidebar.markdown("Operator Details")
    st.sidebar.dataframe(operator_details)
    if 'complete_operator_data.pkl' not in os.listdir('Pickle files'):
        print('Complete operator data File not available')
        data = pd.read_csv('Datasets/datadump_s5_summary_operator_loadout.csv')
        operators = list(data['operator'].unique())
        mean_all_kills = []
        mean_all_deaths = []
        mean_all_picks = []
        for operator in operators:
            mean_all_kills.append(data[data['operator'] == operator]['nbwins'].mean())
            mean_all_deaths.append(data[data['operator'] == operator]['nbdeaths'].mean())
            mean_all_picks.append(data[data['operator'] == operator]['nbpicks'].mean())
        
        complete_dictionary = {'mean_all_picks': mean_all_picks, 'mean_all_deaths': mean_all_deaths,
                               'mean_all_kills': mean_all_kills, 'operators':operators}
        pickle_file = open('Pickle files/complete_operator_data.pkl' , 'ab')
        pickle.dump(complete_dictionary, pickle_file)
        pickle_file.close()
    
    complete_file = open('Pickle files/complete_operator_data.pkl' , 'rb')
    complete_dictionary = pickle.load(complete_file)
    complete_file.close()
    print('Complete operator data File loaded')
    
    stacked_bar = go.Figure(data = [
        go.Bar(name = 'Mean kills', x = complete_dictionary['operators'], y = complete_dictionary['mean_all_kills']),
        go.Bar(name = 'Mean deaths', x = complete_dictionary['operators'], y = complete_dictionary['mean_all_deaths']),
        go.Bar(name = 'Mean picks', x = complete_dictionary['operators'], y = complete_dictionary['mean_all_picks'])
        ])
    stacked_bar.update_layout(barmode = 'group')
    # plot(stacked_bar)
    st.markdown('Mean kills, deaths, pick rate for all operators'.upper())
    st.plotly_chart(stacked_bar)
    
    
    print('Done displaying all! Enjoyy!')
    

def plot_objectives_data(map_location):
    if 'objective_data' + map_location + '.pkl' not in os.listdir('Pickle files'):
        print('Objective data File not available')
        data = pd.read_csv('Datasets/datadump_s5_summary_objectives.csv')
        map_details = data[data['mapname'] == map_location]
        attackers = map_details[map_details['role'] == 'Attacker']
        defenders = map_details[map_details['role'] == 'Defender']
        total_attacker_wins = attackers['nbwins'].sum()
        total_defender_wins = defenders['nbwins'].sum()
        total_attacker_kills = attackers['nbkills'].sum()
        total_defender_kills = defenders['nbkills'].sum()
        total_attacker_deaths = attackers['nbdeaths'].sum()
        total_defender_deaths = defenders['nbdeaths'].sum()
        top_3_attackers = attackers['operator'].value_counts()[:3].index.tolist()
        top_3_defenders = defenders['operator'].value_counts()[:3].index.tolist()
        number_bombs = map_details[map_details['gamemode'] == 'BOMB']['dateid'].count()
        number_secure_area = map_details[map_details['gamemode'] == 'SECURE_AREA']['dateid'].count()
        number_hostage = map_details[map_details['gamemode'] == 'HOSTAGE']['dateid'].count()
        chosen_per_rank = dict(map_details['skillrank'].value_counts())
        objective_location_count = dict(map_details['objectivelocation'].value_counts())
        
        objective_dictionary = {'total_attacker_wins': total_attacker_wins, 
                               'total_defender_wins': total_defender_wins, 
                               'total_attacker_kills': total_attacker_kills, 
                               'total_defender_kills': total_defender_kills,
                               'total_attacker_deaths': total_attacker_deaths,
                               'total_defender_deaths': total_defender_deaths,
                               'top_3_attackers': top_3_attackers, 
                               'top_3_defenders': top_3_defenders, 'number_bombs': number_bombs,
                               'number_secure_area': number_secure_area, 'number_hostage': number_hostage,
                               'chosen_per_rank': chosen_per_rank, 
                               'objective_location_count': objective_location_count
                               }
        pickle_file = open('Pickle files/objective_data' + map_location + '.pkl', "ab")
        pickle.dump(objective_dictionary , pickle_file)
        pickle_file.close()
        print('Objective data File loaded')
    
    file = open('Pickle files/objective_data' + map_location + '.pkl', "rb")
    operator_dictionary = pickle.load(file)
    file.close()
    
    objective_data_summary = pd.DataFrame([operator_dictionary['total_attacker_wins'], 
                                           operator_dictionary['total_defender_wins'],
                                           operator_dictionary['total_attacker_kills'], 
                                           operator_dictionary['total_defender_kills'],
                                           operator_dictionary['total_attacker_deaths'], 
                                           operator_dictionary['total_defender_deaths'],
                                           operator_dictionary['number_bombs'], 
                                           operator_dictionary['number_hostage'], 
                                           operator_dictionary['number_secure_area']],
                                          columns = ['Details'],
                                          index = ['Attacker wins', 'Defender wins',
                                                   'Attacker kills', 'Defender kills',
                                                   'Attacker deaths', 'Defender deaths',
                                                   'Bombs', 'Hostages',
                                                   'Secure areaa'])
    
    st.sidebar.markdown('Map statistics')
    st.sidebar.dataframe(objective_data_summary)
    
    rank_chosen_dataframe = pd.DataFrame(list(operator_dictionary['chosen_per_rank'].values()), 
                                         columns = ['Number'], 
                                         index = list(operator_dictionary['chosen_per_rank'].keys()))
    st.sidebar.markdown('Map statistics per rank')
    st.sidebar.dataframe(rank_chosen_dataframe)
    
    objective_location_dataframe = pd.DataFrame(list(operator_dictionary['objective_location_count'].values()), 
                                                columns = ['Number'], 
                                                index = [location[0:13] for location in list(operator_dictionary['objective_location_count'].keys())])
    st.sidebar.markdown('Map statistics for locations')
    st.sidebar.dataframe(objective_location_dataframe)
    
    if 'objective_data_all.pkl' not in os.listdir('Pickle files'):
        print('Complete objective File not available')
        data = pd.read_csv('Datasets/datadump_s5_summary_objectives.csv')
        mean_attacker_win_all = []
        mean_defender_win_all = []
        for chosen_map in map_list:
            details = data[data['mapname'] == chosen_map]
            attacker_data = details[details['role'] == 'Attacker']
            defender_data = details[details['role'] == 'Defender']
            mean_attacker_win_all.append(attacker_data['nbwins'].mean())
            mean_defender_win_all.append(defender_data['nbwins'].mean())
            objective_all_dictionary = {'mean_attacker_win_all': mean_attacker_win_all,
                                        'mean_defender_win_all': mean_defender_win_all}
        pickle_file = open('Pickle files/objective_data_all.pkl', "ab")
        pickle.dump(objective_all_dictionary, pickle_file)
        pickle_file.close()
        
        
    objective_all_file = open('Pickle files/objective_data_all.pkl', "rb")
    objective_all_dictionary = pickle.load(objective_all_file)
    objective_all_file.close()
    print('Complete objective data File loaded')
        
    stacked_bar = go.Figure(data = [
        go.Bar(name = 'Mean attacker win', x = map_list, y = objective_all_dictionary['mean_attacker_win_all']),
        go.Bar(name = 'Mean defender win', x = map_list, y = objective_all_dictionary['mean_defender_win_all']),
        ])
    stacked_bar.update_layout(barmode = 'group')
    #plot(stacked_bar)
    
    attack_vs_defend = [operator_dictionary['total_attacker_wins'], 
                        operator_dictionary['total_defender_wins']]
    at_v_def_label = ['Attackers win', 'Defenders win']
    pie_at_v_def = go.Figure(data = [go.Pie(labels = at_v_def_label, values = attack_vs_defend)])
    # plot(pie_at_v_def)
    
    objective_data = [operator_dictionary['number_bombs'], operator_dictionary['number_hostage'], 
                      operator_dictionary['number_secure_area']]
    objective_labels = ['Bomb', 'Hostage extraction', 'Secure area']
    pie_objective = go.Figure(data = [go.Pie(labels = objective_labels, values = objective_data)])
    # plot(pie_objective)
    st.markdown('All Maps attacker vs defender chart'.upper())
    st.plotly_chart(stacked_bar)
    
    st.markdown('Attackers vs defenders for '.upper() + map_location.upper())
    st.plotly_chart(pie_at_v_def)
    
    st.markdown('Objective distribution '.upper() + map_location.upper())
    st.plotly_chart(pie_objective)
    
    
    
def player_data_details():
    ranked_dist = {'Copper 5':0.2, 'Copper 4': 0.2, 'Copper 3': 0.2, 'Copper 2': 0.3, 'Copper 1': 0.4, 
               'Bronze 5': 0.6, 'Bronze 4': 0.8, 'Bronze 3': 1.0, 'Bronze 2': 1.3, 'Bronze 1': 1.8, 
               'Silver 5': 2.4, 'Silver 4': 3.1, 'Silver 3': 4.0, 'Silver 2': 4.7, 'Silver 1': 5.6, 
               'Gold 3': 13.9, 'Gold 2': 14.9, 'Gold 1': 13.7,  
               'Platinum 3': 20.2, 'Platinum 2':7.7, 'Platinum 1': 2.3, 
               'Diamond': 0.59,
               'Champion': 0.01}
    colors = [['#845228'] *5]
    colors.append(['#cd7f32'] * 5)
    colors.append(['silver'] * 5)
    colors.append(['gold'] * 3)
    colors.append(['#CDD5E0'] * 3)
    colors.append(['#B9F2FF'])
    colors.append(['pink'])
    final_colors = [color for sublist in colors for color in sublist]
    ranked_dist_plot = go.Figure(go.Bar(name = 'Ranked distribution', x = list(ranked_dist.keys()),
                                   y = list(ranked_dist.values()), marker_color = final_colors))
    
    st.markdown('Ranked distribution among the world'.upper())
    st.plotly_chart(ranked_dist_plot)
    
    request = Request('https://r6.apitab.com/leaderboards/windows/all', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(request).read()
    response = json.loads(webpage)
    print('Response received')
    records = []
    for key in response['players'].keys():
        ranked_data = response['players'][key]
        name = ranked_data['profile']['p_name']
        level = ranked_data['stats']['level']
        rank = ranked_data['ranked']['rank']
        mmr = ranked_data['ranked']['mmr']
        kd = ranked_data['ranked']['kd']
        server = ""
        if ranked_data['ranked']['NA_mmr'] != 0:
            server = 'North America'
        elif ranked_data['ranked']['EU_mmr'] != 0:
            server = 'Europe'
        else:
            server = 'Asia'
        records.append([name, level, rank, mmr, kd, server])
    ranked_summary = pd.DataFrame(records,
                                  columns = ['Player name', 'Player level', 'Player rank', 'Player mmr',
                                            'Player kd', 'Server played'])
    
    NA = EU = AS = 0
    for key in response['players'].keys():
        ranked_data = response['players'][key]['ranked']
        if ranked_data['NA_mmr'] != 0:
            NA += 1
            continue
        elif ranked_data['EU_mmr'] != 0:
            EU += 1
            continue
        else:
            AS += 1
    world = awoc.AWOC()
    countries_NA = world.get_countries_list_of('North America')
    countries_EU = world.get_countries_list_of('Europe')
    countries_AS = world.get_countries_list_of('Asia')
    countries = []
    countries.append(countries_NA)
    countries.append(countries_EU)
    countries.append(countries_AS)
    countries_flatten = [country for continent in countries for country in continent]
    count_final = []
    for _ in countries_NA:
        count_final.append(NA)
    for _ in countries_EU:
        count_final.append(EU)
    for _ in countries_AS:
        count_final.append(AS)
        
    data = dict(type='choropleth',
    locations = countries_flatten,
    locationmode = 'country names', z = count_final,
    text = countries_flatten, colorbar = {'title':'Number of players'},
    colorscale= 'Reds',    
    reversescale = False)
    layout = dict(title='Top ranked players per server',
    geo = dict(showframe = True, projection={'type':'mercator'}))
    choromap = go.Figure(data = [data], layout = layout)
    # plot(choromap, validate=False)
    st.markdown('Worldwide distribution of top 100 players'.upper())
    st.plotly_chart(choromap)
    
    st.markdown('Top 100 ranked players'.upper())
    st.dataframe(ranked_summary)
    print('Data displayed! Enjoyyyyyy!')

operators_list = ['BOPE-CAPITAO', 'G.E.O.-JACKAL', 'GIGN-MONTAGNE', 'GIGN-RESERVE', 'GIGN-TWITCH',
 'GSG9-BLITZ', 'GSG9-IQ', 'GSG9-RESERVE', 'JTF2-BUCK', 'NAVYSEAL-BLACKBEARD', 'SAS-RESERVE',
 'SAS-SLEDGE', 'SAS-THATCHER', 'SAT-HIBANA', 'SPETSNAZ-FUZE', 'SPETSNAZ-GLAZ', 'SPETSNAZ-RESERVE', 'SWAT-ASH',
 'SWAT-RESERVE', 'SWAT-THERMITE', 'BOPE-CAVEIRA', 'G.E.O.-MIRA', 'GIGN-DOC', 'GIGN-ROOK', 'GSG9-BANDIT',
 'GSG9-JAGER', 'JTF2-FROST', 'NAVYSEAL-VALKYRIE', 'SAS-MUTE', 'SAS-SMOKE', 'SAT-ECHO', 'SPETSNAZ-KAPKAN',
 'SPETSNAZ-TACHANKA', 'SWAT-CASTLE', 'SWAT-PULSE']
map_list = ['BANK', 'BARTLETT_U.', 'BORDER', 'CHALET', 'CLUB_HOUSE', 'COASTLINE', 'CONSULATE',
 'FAVELAS','HEREFORD_BASE', 'HOUSE', 'KAFE_DOSTOYEVSKY', 'KANAL', 'OREGON', 'PLANE', 'SKYSCRAPER',
 'YACHT']

st.sidebar.title('Choose option')
option = st.sidebar.radio("", ['Map details', 'Operator details', 'Top ranked players'])

if option == 'Map details':
    st.sidebar.markdown('Select the map')
    map_location = st.sidebar.selectbox('Choose map', map_list)
    plot_objectives_data(map_location)
    
if option == 'Operator details':
    st.sidebar.markdown('Select the operator')
    operator_name = st.sidebar.selectbox('Choose operator', operators_list)
    plot_operator(operator_name)

if option == 'Top ranked players':
    player_data_details()