import re

class Player:
    def __init__(self, id, number, firstName, lastName, height, weight, birthDate, college):
        self.id = id
        self.number = number
        self.firstName = firstName
        self.lastName = lastName
        self.height = height
        self.weight = weight
        self.birthDate = birthDate
        self.college = college

class Play:
    def __init__(self):
        self.abc = 1

def loadFile(fileName, fileSep):
    return [line.split(fileSep) for line in open(fileName).readlines()]

def columnIndices(csvHeader):
    return { column : index for index, column in enumerate(csvHeader)}

def seperateHeadBody(data):
    return columnIndices(data[0]), data[1:-1]

def selection(columns, data, column, withValue):
    return [row for row in data if row[columns[column]] == withValue]

def projection(columns, data, columnsToInclude):
    indices = [columns[column] for column in columnsToInclude]
    return columnIndices(columnsToInclude), [[row[index] for index in indices] for row in data]

#id for team = city.year
teams = {line[:-1] + "2018" : line[:-1] for line in open('2018/team_cities.txt').readlines()}

players = dict()
#id for player city.year.number.lastname
for team_id in teams:
    city = teams[team_id]
    rawRosterData = loadFile('2018/' + city + ".csv", ',')
    rosterColumns, rosterData = seperateHeadBody(rawRosterData)
    for row in rosterData:
        name = row[rosterColumns['Player']]
        firstName = name.split('\\')[0].split(' ')[0]
        lastName = name.split('\\')[0].split(' ')[1]
        number = row[rosterColumns['No.']]
        height = row[rosterColumns['Ht']]
        weight = row[rosterColumns['Wt']]
        birthDate = row[rosterColumns['BirthDate']]
        college = row[rosterColumns['College/Univ']]
        id = city + "2018" + number + lastName
        players[id] = Player(id, number, firstName, lastName, height, weight, birthDate)

'''
#Loads raw play by play data
raw_pbp_data = loadFile('2018/pbp-2018_tabs.txt', '\t')
columns, data = seperateHeadBody(raw_pbp_data)

#Extracts only the first game's plays (phi vs atl)
singleGameColumns, singleGame = projection(columns, selection(columns, data, 'GameId', '2018090600'), ['GameId', 'Quarter', 'Minute', 'Second', 'Description', 'OffenseTeam', 'DefenseTeam', 'Yards', 'PlayType'])


playTypes = set([row[singleGameColumns['PlayType']] for row in singleGame])
print(playTypes)


passes = selection(singleGameColumns, singleGame, 'PlayType', 'PASS')
for row in passes:
    playDescription = row[singleGameColumns['Description']]
    playersInvolved = re.findall("\d*-\w\.[A-Z]\w*", playDescription)
'''