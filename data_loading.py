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
        return "INSERT INTO Player (PlayerID, PlayerNumber, FirstName, LastName, Height, Weight, BirthDate, College) VALUES ('{0}', {1}, '{2}', '{3}', {4}, {5}, '{6}', '{7}');".format(self.id, self.number, self.firstName, self.lastName, self.height, self.weight, self.birthDate, self.college)

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
        return "INSERT INTO Play (PlayID, GameID, DefenderID, Quarter, Minute, Second, Yards, GoalScored, PlayType, PlayTypeID) VALUES ({0}, '{1}', '{2}', {3}, {4}, {5}, {6}, {7}, '{8}', {9});".format(self.playId, self.gameId, self.defenderId, self.quarter, self.minute, self.second, self.yards, self.goalScored, self.playType, self.playChildId)


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
plays = []
passPlays = []
currentId = 0
teams = {line[:-1] + currentYear : line[:-1] for line in open('2018/team_cities.txt').readlines()}
players = dict()
games = []
raw_pbp_data = loadFile('2018/pbp-2018_tabs.txt', '\t')
rawColumns, rawData = seperateHeadBody(raw_pbp_data)

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

#Extracts only the pass plays
passes = selection(rawColumns, rawData, 'PlayType', 'PASS')
i = 0
for row in passes:
    print(i)
    i += 1
    playDescription = row[rawColumns['Description']]
    playersInvolved = re.findall("\d*-\w\.[A-Z]\w*", playDescription)
    defenderId = None
    passerId = None
    receiverId = None
    complete = False
    if(row[rawColumns['GameId']] not in games):
        games.append(row[rawColumns['GameId']])
    if "INCOMPLETE" not in playDescription:
        complete = True
        passerId = row[rawColumns['OffenseTeam']] + currentYear + playersInvolved[0]
        receiverId = row[rawColumns['OffenseTeam']] + currentYear + playersInvolved[1]
        if len(playersInvolved) >= 3:
            defenderId = row[rawColumns['DefenseTeam']] + currentYear + playersInvolved[2]
        if passerId not in players:
            print(passerId)
            input('pausing')
        if receiverId not in players:
            print(receiverId)
            input('pausing')
        if defenderId not in players:
            print(defenderId)
            input('pausing')
    if passerId != None:
        newPlay = Play(currentId, row[rawColumns['GameId']], defenderId, row[rawColumns['Quarter']], row[rawColumns['Minute']], row[rawColumns['Second']], row[rawColumns['Yards']], 0, "PASS", currentId + 1)
        newPassPlay = PassPlay(currentId + 1, currentId, passerId, receiverId, 1 if complete else 0)
        plays.append(newPlay)
        passPlays.append(newPassPlay)
    currentId += 2

for game in games:
    print("INSERT INTO GAME(GameID) values ('{0}}');".format(game))

for team in teams:
    print("INSERT INTO Team (TeamId, City) VALUES ('{0}', '{1}');".format(team, teams[team]))

for player in players:
    print(players[player].getInsert())

for play in plays:
    print(play.getInsert())

for p in passPlays:
    print(p.getInsert())