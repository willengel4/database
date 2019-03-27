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
    def getInsert(self):
        return "INSERT INTO Player (PlayerID, Number, FirstName, LastName, Height, Weight, BirthDate, College) VALUES ('{0}', {1}, '{2}', '{3}', {4}, {5}, TO_DATE('{6}', 'DD/MM/YYYY'), '{7}');".format(self.id, self.number, self.firstName, self.lastName, self.height, self.weight, self.birthDate, self.college)

class Play:
    def __init__(self, playId, gameId, defenderId, quarter, minute, second, yards, goalScored, playType, playChildId):
        self.playId = playId
        self.gameId = gameId
        self.defenderId = defenderId
        self.quarter = quarter
        self.minute = minute
        self.second = second
        self.yards = yards
        self.goalScored = goalScored
        self.playType = playType
        self.playChildId = playChildId
    def getInsert(self):
        return "INSERT INTO Play (PlayID, GameID, DefenderID, Quarter, Minute, Second, Yards, GoalScored, PlayType, PlayTypeID) VALUES ({0}, '{1}', '{2}', {3}, {4}, {5}, {6}, {7}, '{8}', {9});".format(self.playId, self.gameId, self.defenderId, self.quarter, self.minute, self.second, self.yards, False, self.playType, self.playChildId)


class PassPlay:
    def __init__(self, passId, playId, passerId, receiverId, completed):
        self.passId = passId
        self.playId = playId
        self.passerId = passerId
        self.receiverId = receiverId
        self.completed = completed
    def getInsert(self):
        return "INSERT INTO PassPlay (PassID, PlayID, PasserID, ReceiverID, Completed) VALUES ({0}, {1}, '{2}', '{3}', {4});".format(self.passId, self.playId, self.passerId, self.receiverId, self.completed)

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

def toInches(str):
    t = str.split('-')
    return int(t[0]) * 12 + int(t[1])

currentYear = "2018"

#id for team = city.year
teams = {line[:-1] + currentYear : line[:-1] for line in open('2018/team_cities.txt').readlines()}

players = dict()
#id for player city.year.number.lastname
for team_id in teams:
    city = teams[team_id]
    rawRosterData = loadFile(currentYear + '/' + city + ".csv", ',')
    rosterColumns, rosterData = seperateHeadBody(rawRosterData)
    count = 0
    for row in rosterData:
        name = row[rosterColumns['Player']]
        firstName = name.split('\\')[0].split(' ')[0]
        lastName = name.split('\\')[0].split(' ')[1]
        number = row[rosterColumns['No.']]
        height = toInches(row[rosterColumns['Ht']])
        weight = row[rosterColumns['Wt']]
        birthDate = row[rosterColumns['BirthDate']]
        college = row[rosterColumns['College/Univ']]
        id = (city + currentYear + number + "-" + firstName[0] + "." + lastName).upper()
        players[id] = Player(id, number, firstName, lastName, height, weight, birthDate, college)

plays = []
passPlays = []
currentId = 0

#Loads raw play by play data
raw_pbp_data = loadFile('2018/pbp-2018_tabs.txt', '\t')
columns, data = seperateHeadBody(raw_pbp_data)

#Extracts only the first game's plays (phi vs atl)
singleGameColumns, singleGame = projection(columns, selection(columns, data, 'GameId', '2018090600'), ['GameId', 'Quarter', 'Minute', 'Second', 'Description', 'OffenseTeam', 'DefenseTeam', 'Yards', 'PlayType'])

#Extracts only the pass plays
passes = selection(singleGameColumns, singleGame, 'PlayType', 'PASS')
for row in passes:
    playDescription = row[singleGameColumns['Description']]
    playersInvolved = re.findall("\d*-\w\.[A-Z]\w*", playDescription)
    defenderId = None
    passerId = None
    receiverId = None
    complete = False
    if "INCOMPLETE" not in playDescription:
        complete = True
        passerId = row[singleGameColumns['OffenseTeam']] + currentYear + playersInvolved[0]
        receiverId = row[singleGameColumns['OffenseTeam']] + currentYear + playersInvolved[1]
        if len(playersInvolved) >= 3:
            defenderId = row[singleGameColumns['DefenseTeam']] + currentYear + playersInvolved[2]
        
        if passerId not in players:
            print(passerId)
            input()
        if receiverId not in players:
            print(receiverId)
            input()
        if defenderId not in players:
            print(defenderId)
            input()
    newPlay = Play(currentId, row[singleGameColumns['GameId']], defenderId, row[singleGameColumns['Quarter']], row[singleGameColumns['Minute']], row[singleGameColumns['Second']], row[singleGameColumns['Yards']], False, "PASS", currentId + 1)
    newPassPlay = PassPlay(currentId + 1, currentId, passerId, receiverId, complete)
    plays.append(newPlay)
    passPlays.append(newPassPlay)
    currentId += 2

for team in teams:
    print("INSERT INTO Team (TeamId, City) VALUES ('{0}', '{1}');".format(team, teams[team]))

for player in players:
    print(players[player].getInsert())

for play in plays:
    print(play.getInsert())

for p in passPlays:
    print(p.getInsert())