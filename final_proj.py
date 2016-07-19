# unicodecsv works exactly the same as csv, but it comes with Anaconda and has support for unicode.
import unicodecsv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict


def read_csv(filename):
    # rb mode means the file will be opened for reading, b flag changes the format how the file is read
    with open(filename,'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)


salaries = read_csv('Salaries.csv')
schools = read_csv('Schools.csv')
pitching = read_csv('Pitching.csv')


from datetime import datetime as dt

# Takes a date as a string, and returns a Python datetime object.
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')
# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)


# CLEANING DATA

# Changing the datatypes for each file
for salary in salaries:
    salary['yearID'] = parse_maybe_int(salary['yearID'])
    salary['salary'] = parse_maybe_int(salary['salary'])



for pitching_record in pitching:
    pitching_record['yearID'] = parse_maybe_int(pitching_record['yearID'])
    pitching_record['stint'] = parse_maybe_int(pitching_record['stint'])
    pitching_record['W'] = parse_maybe_int(pitching_record['W'])
    pitching_record['L'] = parse_maybe_int(pitching_record['L'])
    pitching_record['G'] = parse_maybe_int(pitching_record['G'])
    pitching_record['GS'] = parse_maybe_int(pitching_record['GS'])
    pitching_record['CG'] = parse_maybe_int(pitching_record['CG'])
    pitching_record['SHO'] = parse_maybe_int(pitching_record['SHO'])
    pitching_record['SV'] = parse_maybe_int(pitching_record['SV'])
    pitching_record['IPouts'] = parse_maybe_int(pitching_record['IPouts'])
    pitching_record['H'] = parse_maybe_int(pitching_record['H'])
    pitching_record['ER'] = parse_maybe_int(pitching_record['ER'])
    pitching_record['HR'] = parse_maybe_int(pitching_record['HR'])
    pitching_record['BB'] = parse_maybe_int(pitching_record['BB'])

all_salaries = []
for salary in salaries:
        all_salaries.append(salary['salary'])




#Summarize the given data
def describe_data(data):
    print 'Mean:',np.mean(data)
    print 'Standard Deviation:',np.std(data)
    print 'Minimum:',np.min(data)
    print 'Maximum:',np.max(data)

# Summarize and plot graph
def describe_data_graph(data):
    print 'Mean:',np.mean(data)
    print 'Standard Deviation:',np.std(data)
    print 'Minimum:',np.min(data)
    print 'Maximum:',np.max(data)
    plt.hist(data)
    plt.show()






# Group data by playerID

def group_data(data, key_name):
    grouped_data = defaultdict(list)
    for data_point in data:
        key = data_point[key_name]
        grouped_data[key].append(data_point)
    return grouped_data


def sum_grouped_items(grouped_data, field_name):
    summed_data = {}
    for key, data_points in grouped_data.items():
        total = 0
        for data_point in data_points:
            total += data_point[field_name]
        summed_data[key] = total
    return summed_data




# Create two lists of data,
#  - one for players with more than 75th percentile salary
#  - one for players with less than 25th percentile salary

high_salary_players = set()
for player in salaries:
    if player['salary'] >= np.percentile(all_salaries,75):
        high_salary_players.add(player['playerID'])
# print(high_salary_players)

low_salary_players = set()
for player in salaries:
    if player['salary'] <= np.percentile(all_salaries,25):
        low_salary_players.add(player['playerID'])
# print(low_salary_players)





# highest_salary = []
# lowest_salary = []

# for salary_record in salaries:
#     if salary_record['playerID'] in high_salary_players:
#         highest_salary.append(salary_record)
#     elif salary_record['playerID'] in low_salary_players:
#         lowest_salary.append(salary_record)

# highest_salary = pd.Series(highest_salary)
# lowest_salary = pd.Series(lowest_salary)


# Group data by playerID (high salary)
pitching_high_salary_rows = []

for pitching_record in pitching:
    if pitching_record['playerID'] in high_salary_players:
        pitching_high_salary_rows.append(pitching_record)
pitching_high_salary_rows = pd.Series(pitching_high_salary_rows)

pitching_high_salary_by_id  = group_data(pitching_high_salary_rows,'playerID')



# Group data by playerID (low salary)
pitching_low_salary_rows = []
for pitching_record in pitching:
    if pitching_record['playerID'] in low_salary_players:
        pitching_low_salary_rows.append(pitching_record)
pitching_low_salary_rows = pd.Series(pitching_low_salary_rows)

pitching_low_salary_by_id = group_data(pitching_low_salary_rows,'playerID')


# # # Stats for games played in pitching with players in highest_salary list
# print 'High salary players (G) Stats'
# print '_______________________'
# pitching_high_salary_G = sum_grouped_items(pitching_high_salary_by_id, 'G')
# print(describe_data(pitching_high_salary_G.values()))



# # Stats for games played in pitching with players in lowest_salary list
# print 'Low salary players (G) Stats'
# print '______________________'
# pitching_low_salary_G = sum_grouped_items(pitching_low_salary_by_id,'G')
# print(describe_data(pitching_low_salary_G.values()))



# print 'High salary players (Hits)'
# print '__________________________'
# pitching_high_salary_H = sum_grouped_items(pitching_high_salary_by_id,'H')
# print(describe_data(pitching_high_salary_H.values()))

# print 'Low salary players (Hits)'
# print '_________________________'
# pitching_low_salary_H = sum_grouped_items(pitching_low_salary_by_id,'H')
# print(describe_data(pitching_low_salary_H.values()))



# print 'High salary players (Homeruns)'
# print '__________________________'
# pitching_high_salary_HR = sum_grouped_items(pitching_high_salary_by_id,'HR')
# print(describe_data(pitching_high_salary_HR.values()))

# print 'Low salary players (Homeruns)'
# print '__________________________'
# pitching_low_salary_HR = sum_grouped_items(pitching_low_salary_by_id,'HR')
# print(describe_data(pitching_low_salary_HR.values()))





# CORRELATION


# correlation between wins and hits
wins = []
for pitch in pitching:
    wins.append(pitch['W'])
wins = np.asarray(wins)  # convert list to numpy array

hits = []
for pitch in pitching:
    hits.append(pitch['H'])
hits = np.asarray(hits)


# print(np.corrcoef(wins,hits))





# Pandas combine tables
hallOfFame = pd.read_csv('HallOfFame.csv')
salaries = pd.read_csv('Salaries.csv')


# Join two tables on id
def combine_dfs(data1, data2):
    return data1.merge(data2, on = ['playerID'], how= "inner")


hallOfFame_salaries_combined = combine_dfs(hallOfFame,salaries)

print "Pearson's r for salary and total votes received"
print(np.corrcoef(hallOfFame_salaries_combined['salary'],hallOfFame_salaries_combined['votes']))

awardsSharePlayers = pd.read_csv('AwardsSharePlayers.csv')
awards_salaries_combined = combine_dfs(awardsSharePlayers,salaries)

print "Pearson's r for salary and points won"
print(np.corrcoef(awards_salaries_combined['salary'],awards_salaries_combined['pointsWon']))






college_playing = pd.read_csv('CollegePlaying.csv')
# print(college_playing['schoolID'])
college_count = college_playing['schoolID'].value_counts()


college_count[:20].plot(kind='barh',rot =0)
plt.show()