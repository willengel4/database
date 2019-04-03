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
        return "INSERT INTO Play (PlayID, GameID, DefenderID, Quarter, Minute, Second, Yards, GoalScored, PlayType, PlayTypeID) VALUES ({0}, '{1}', {2}, {3}, {4}, {5}, {6}, {7}, '{8}', {9});".format(self.playId, self.gameId, self.defenderId, self.quarter, self.minute, self.second, self.yards, self.goalScored, self.playType, self.playChildId)


class PassPlay:
    def __init__(self, passId, playId, passerId, receiverId, completed):
        self.passId = passId
        self.playId = playId
        self.passerId = passerId
        self.receiverId = receiverId
        self.completed = completed
    def getInsert(self):
        return "INSERT INTO PassPlay (PassID, PlayID, PasserID, ReceiverID, Completed) VALUES ({0}, {1}, {2}, {3}, {4});".format(self.passId, self.playId, self.passerId, self.receiverId, self.completed)

class RunPlay:
    def __init__(self, runId, playId, runnerId):
        self.runId = runId
        self.playId = playId
        self.runnerId = runnerId
    def getInsert(self):
        return "INSERT INTO RunPlay (RunID, PlayID, RunnerID) VALUES ({0}, {1}, {2});".format(self.runId, self.playId, self.runnerId)

class KickPlay:
    def __init__(self, kickId, playId, kickerId):
        self.kickId = kickId
        self.playId = playId
        self.kickerId = kickerId
    def getInsert(self):
        return "INSERT INTO KickPlay (KickID, PlayID, KickerID) VALUES ({0}, {1}, {2});".format(self.kickId, self.playId, self.kickerId)

class TimeOut:
    def __init__(self, timeoutId, playId):
        self.timeoutId = timeoutId
        self.playId = playId
    def getInsert(self):
        return "INSERT INTO TimeOut (TimeOutID, PlayID, Duration) VALUES ({0}, {1}, {2});".format(self.timeoutId, self.playId, 0)

def loadFile(fileName, fileSep):
    return [line.split(fileSep) for line in open(fileName).readlines()]

def columnIndices(csvHeader):
    return { column : index for index, column in enumerate(csvHeader)}

def seperateHeadBody(data):
    return columnIndices(data[0]), data[1:]

def selection(columns, data, column, withValue):
    return [row for row in data if row[columns[column]] == withValue]

def projection(columns, data, columnsToInclude):
    indices = [columns[column] for column in columnsToInclude]
    return columnIndices(columnsToInclude), [[row[index] for index in indices] for row in data]

def toInches(str):
    t = str.split('-')
    return int(t[0]) * 12 + int(t[1])

def formatId(id):
    if id == None:
        return "NULL"
    else:
        return "'{0}'".format(id)

currentYear = "2018"
plays = []
passPlays = []
runPlays = []
kickPlays = []
timeouts = []
currentId = 0
teams = {line[:-1] + currentYear : line[:-1] for line in open('2018/team_cities.txt').readlines()}
players = dict()
games = []
raw_pbp_data = loadFile('2018/pbp-2018_tabs.txt', '\t')
rawColumns, rawData = seperateHeadBody(raw_pbp_data)

no_matching_ids = list()

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
        if '-' in lastName:
            lastName = lastName[0:lastName.find('-')]
        number = row[rosterColumns['No.']]
        height = toInches(row[rosterColumns['Ht']])
        weight = row[rosterColumns['Wt']]
        birthDate = row[rosterColumns['BirthDate']]
        college = row[rosterColumns['College/Univ']]
        if '&' in college:
            college = college.replace('&', '')
        id = (city + currentYear + number + "-" + firstName[0] + "." + lastName).upper()
        players[id] = Player(id, number, firstName, lastName, height, weight, birthDate, college)

#Extracts only the pass plays
passes = selection(rawColumns, rawData, 'PlayType', 'PASS')
for row in passes:
    playDescription = row[rawColumns['Description']]
    playersInvolved = re.findall("\d*-[A-Z]\w*\.[A-Z]\w*", playDescription)
    for i, p in enumerate(playersInvolved):
        if "'" in p:
            playersInvolved[i] = p.replaceAll("'", "")
    defenderId = None
    passerId = None
    receiverId = None
    complete = "INCOMPLETE" not in playDescription
    goalScored = "TOUCHDOWN" in playDescription
    if(row[rawColumns['GameId']] not in games):
        games.append(row[rawColumns['GameId']])
    if "INTERCEPT" in playDescription or "FUMBLE" in playDescription or "PENALTY" in playDescription:
        continue
    if len(playersInvolved) >= 1:
        passerId = row[rawColumns['OffenseTeam']] + currentYear + playersInvolved[0]
    if len(playersInvolved) >= 2:
        receiverId = row[rawColumns['OffenseTeam']] + currentYear + playersInvolved[1]
    if len(playersInvolved) >= 3:
        defenderId = row[rawColumns['DefenseTeam']] + currentYear + playersInvolved[2]
    if(defenderId is not None and defenderId not in players) or (passerId is not None and passerId not in players) or (receiverId is not None and receiverId not in players):
        no_matching_ids.append(playDescription + " - " + str(playersInvolved) + " - " + row[rawColumns['OffenseTeam']] + " - " + row[rawColumns['DefenseTeam']])
        if defenderId is not None and defenderId not in players:
            no_matching_ids.append('\t' + defenderId)
        if passerId is not None and passerId not in players:
            no_matching_ids.append('\t' + passerId)
        if receiverId is not None and receiverId not in players:
            no_matching_ids.append('\t' + receiverId)
        continue
    if passerId != None:
        newPlay = Play(currentId, row[rawColumns['GameId']], formatId(defenderId), row[rawColumns['Quarter']], row[rawColumns['Minute']], row[rawColumns['Second']], row[rawColumns['Yards']], 1 if goalScored else 0, "PASS", currentId + 1)
        newPassPlay = PassPlay(currentId + 1, currentId, formatId(passerId), formatId(receiverId), 1 if complete else 0)
        plays.append(newPlay)
        passPlays.append(newPassPlay)
    currentId += 2      

#Extracts only the run plays
runs = selection(rawColumns, rawData, 'PlayType', 'RUSH')
for row in runs:
    playDescription = row[rawColumns['Description']]
    playersInvolved = re.findall("\d*-[A-Z]\w*\.[A-Z]\w*", playDescription)
    for i, p in enumerate(playersInvolved):
        if "'" in p:
            playersInvolved[i] = p.replaceAll("'", "")
    defenderId = None
    runnerId = None
    goalScored = "TOUCHDOWN" in playDescription
    if(row[rawColumns['GameId']] not in games):
        games.append(row[rawColumns['GameId']])
    if "INTERCEPT" in playDescription or "FUMBLE" in playDescription or "PENALTY" in playDescription:
        continue
    if len(playersInvolved) >= 1:
        runnerId = row[rawColumns['OffenseTeam']] + currentYear + playersInvolved[0]
    if len(playersInvolved) >= 2:
        defenderId = row[rawColumns['DefenseTeam']] + currentYear + playersInvolved[1]
    if (defenderId is not None and defenderId not in players) or (runnerId is not None and runnerId not in players):
        no_matching_ids.append(playDescription + " - " + str(playersInvolved) + " - " + row[rawColumns['OffenseTeam']] + " - " + row[rawColumns['DefenseTeam']])
        if defenderId is not None and defenderId not in players:
            no_matching_ids.append('\t' + defenderId)
        if runnerId is not None and runnerId not in players:
            no_matching_ids.append('\t' + runnerId)
        continue
    if runnerId != None:
        newPlay = Play(currentId, row[rawColumns['GameId']], formatId(defenderId), row[rawColumns['Quarter']], row[rawColumns['Minute']], row[rawColumns['Second']], row[rawColumns['Yards']], 1 if goalScored else 0, "RUN", currentId + 1)
        newRunPlay = RunPlay(currentId + 1, currentId, formatId(runnerId))
        plays.append(newPlay)
        runPlays.append(newRunPlay)
    currentId += 2

#Extracts only the field goals
field_goals = selection(rawColumns, rawData, 'PlayType', 'FIELD GOAL')
for row in field_goals:
    playDescription = row[rawColumns['Description']]
    playersInvolved = re.findall("\d*-[A-Z]\w*\.[A-Z]\w*", playDescription)
    for i, p in enumerate(playersInvolved):
        if "'" in p:
            playersInvolved[i] = p.replaceAll("'", "")
    defenderId = None
    kickerId = None
    goalScored = "IS GOOD" in playDescription
    if(row[rawColumns['GameId']] not in games):
        games.append(row[rawColumns['GameId']])
    if "INTERCEPT" in playDescription or "FUMBLE" in playDescription or "PENALTY" in playDescription:
        continue
    if len(playersInvolved) >= 1:
        kickerId = row[rawColumns['OffenseTeam']] + currentYear + playersInvolved[0]
    if kickerId is not None and kickerId not in players:
        no_matching_ids.append(playDescription + " - " + str(playersInvolved) + " - " + row[rawColumns['OffenseTeam']] + " - " + row[rawColumns['DefenseTeam']])
        if defenderId is not None and defenderId not in players:
            no_matching_ids.append('\t' + defenderId)
        if kickerId is not None and kickerId not in players:
            no_matching_ids.append('\t' + kickerId)
        continue
    if kickerId != None:
        newPlay = Play(currentId, row[rawColumns['GameId']], formatId(defenderId), row[rawColumns['Quarter']], row[rawColumns['Minute']], row[rawColumns['Second']], row[rawColumns['Yards']], 1 if goalScored else 0, "KICK", currentId + 1)
        newKickPlay = KickPlay(currentId + 1, currentId, formatId(kickerId))
        plays.append(newPlay)
        kickPlays.append(newKickPlay)
    currentId += 2

#Extracts only the timeouts
timeoutPlays = selection(rawColumns, rawData, 'PlayType', 'TIMEOUT')
for row in timeoutPlays:
    if(row[rawColumns['GameId']] not in games):
        games.append(row[rawColumns['GameId']])
    newPlay = Play(currentId, row[rawColumns['GameId']], 'NULL', row[rawColumns['Quarter']], row[rawColumns['Minute']], row[rawColumns['Second']], row[rawColumns['Yards']], 0, "TIMEOUT", currentId + 1)
    newTimeout = TimeOut(currentId + 1, currentId)
    plays.append(newPlay)
    timeouts.append(newTimeout)
    currentId += 2

for game in games:
    print("INSERT INTO GAME(GameID) values ('{0}');".format(game))

for team in teams:
    print("INSERT INTO Team (TeamId, City) VALUES ('{0}', '{1}');".format(team, teams[team]))

for player in players:
    print(players[player].getInsert())

for play in plays:
    print(play.getInsert())

for p in passPlays:
    print(p.getInsert())

for p in runPlays:
    print(p.getInsert())

for k in kickPlays:
    print(k.getInsert())

for t in timeouts:
    print(t.getInsert())