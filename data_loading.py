
import re

class Team:
    def __init__(self, id, name, city, state):
        self.id = id
        self.name = name
        self.city = city
        self.state = state
        self.players = []

class Player:
    def __init__(self, id, name, height, weight, birthDate, college)
        self.id = id
        self.name = name
        self.height = height
        self.weight = weight
        self.birthDate = birthDate
        self.college = college

class Play:
    def __init__()

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
    
