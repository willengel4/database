import re
from datetime import datetime

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

class PuntPlay:
    def __init__(self, puntId, playId, punterId):
        self.puntId = puntId
        self.playId = playId
        self.punterId = punterId
    def getInsert(self):
        return "INSERT INTO PuntPlay (PuntID, PlayID, PunterID) VALUES ({0}, {1}, {2});".format(self.puntId, self.playId, self.punterId)

class TimeOut:
    def __init__(self, timeoutId, playId):
        self.timeoutId = timeoutId
        self.playId = playId
    def getInsert(self):
        return "INSERT INTO TimeOut (TimeOutID, PlayID, Duration) VALUES ({0}, {1}, {2});".format(self.timeoutId, self.playId, 0)

class PlaysFor:
    def __init__(self, playerId, teamId, year, role):
        self.playerId = playerId
        self.teamId = teamId
        self.year = year
        self.role = role
    def getInsert(self):
        return "INSERT INTO Plays_For (PlayerID, TeamID, Year, Role) values ('{0}', '{1}', {2}, '{3}');".format(self.playerId, self.teamId, self.year, self.role)

class Coach:
    def __init__(self, coachId, firstName, lastName):
        self.coachId = coachId
        self.firstName = firstName
        self.lastName = lastName
    def getInsert(self):
        return "INSERT INTO Coach values ({0}, '{1}', '{2}');".format(self.coachId, self.firstName, self.lastName)

class CoachesFor:
    def __init__(self, teamId, coachId, year):
        self.teamId = teamId
        self.coachId = coachId
        self.year = year
    def getInsert(self):
        return "INSERT INTO Coaches_For values ({0}, {1}, {2});".format(self.year, self.teamId, self.coachId)

class Game:
    def __init__(self, gameId, gameDate, gameTime, gameCity, homeTeam, awayTeam):
        self.gameId = gameId
        self.gameDate = gameDate
        self.gameTime = gameTime
        self.gameCity = gameCity
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
    def getGameInsert(self):
        return "INSERT INTO Game values ('{0}', TO_DATE('{1} {2}', 'MM/DD/YYYY HH:MIAM'), '{3}');".format(self.gameId, self.gameDate, self.gameTime, self.gameCity)
    def getParticipateInsert(self):
        return "INSERT INTO Participates_In values ('{0}', '{1}', '{2}');".format(self.homeTeam + '2018', self.gameId, self.awayTeam + '2018')

def loadFile(fileName, fileSep):
    return [line[:-1].split(fileSep) for line in open(fileName).readlines()]

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

def getGameId(games, gameDate, team1):
    gameDateAsDate = datetime.strptime(gameDate, '%m/%d/%Y')
    for game in games:
        posGameDate = datetime.strptime(game.gameDate, '%m/%d/%Y')
        if gameDateAsDate == posGameDate and (team1 == game.awayTeam or team1 == game.homeTeam):
            return game.gameId

    input(gameDate + " " + team1)

currentYear = "2018"
plays = []
passPlays = []
runPlays = []
kickPlays = []
timeouts = []
playsFors = []
puntPlays = []
currentId = 0
teams = {line[:-1] + currentYear : line[:-1] for line in open('2018/team_cities.txt').readlines()}
players = dict()
games = []
participates = []
zipcodes = dict()
raw_pbp_data = loadFile('2018/pbp-2018_tabs.txt', '\t')
rawColumns, rawData = seperateHeadBody(raw_pbp_data)
raw_coach_data = loadFile('2018/coaches.txt', ',')
coachColumns, coachData = seperateHeadBody(raw_coach_data)
raw_schedule_data = loadFile('2018/schedule2018.txt', ',')
scheduleColumns, scheduleData = seperateHeadBody(raw_schedule_data)
raw_zip_data = loadFile('2018/zipcodes.txt', ',')
zipColumns, zipData = seperateHeadBody(raw_zip_data)
no_matching_ids = list()

for row in zipData:
    team = row[0]
    zip = row[1]
    zipcodes[team] = zip

for row in scheduleData:
    winner = row[scheduleColumns['WINNER']]
    loser = row[scheduleColumns['LOSER']]
    location = row[scheduleColumns['LOCATION']]
    homeTeam = loser if location == 'AT' else winner
    awayTeam = winner if location == 'AT' else loser
    gameDate = row[scheduleColumns['DATE']]
    gameTime = row[scheduleColumns['TIME']]
    gameId = currentYear + gameDate.replace('/', '') + homeTeam
    games.append(Game(gameId, gameDate, gameTime, zipcodes[homeTeam], homeTeam, awayTeam))

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
        newPlaysFor = PlaysFor(id, team_id, currentYear, row[rosterColumns['Pos']])
        playsFors.append(newPlaysFor)

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
        gameId = getGameId(games, row[rawColumns['GameDate']], row[rawColumns['DefenseTeam']])
        newPlay = Play(currentId, gameId, formatId(defenderId), row[rawColumns['Quarter']], row[rawColumns['Minute']], row[rawColumns['Second']], row[rawColumns['Yards']], 1 if goalScored else 0, "PASS", currentId + 1)
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
        gameId = getGameId(games, row[rawColumns['GameDate']], row[rawColumns['DefenseTeam']])
        newPlay = Play(currentId, gameId, formatId(defenderId), row[rawColumns['Quarter']], row[rawColumns['Minute']], row[rawColumns['Second']], row[rawColumns['Yards']], 1 if goalScored else 0, "RUN", currentId + 1)
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
        gameId = getGameId(games, row[rawColumns['GameDate']], row[rawColumns['DefenseTeam']])
        newPlay = Play(currentId, gameId, formatId(defenderId), row[rawColumns['Quarter']], row[rawColumns['Minute']], row[rawColumns['Second']], row[rawColumns['Yards']], 1 if goalScored else 0, "KICK", currentId + 1)
        newKickPlay = KickPlay(currentId + 1, currentId, formatId(kickerId))
        plays.append(newPlay)
        kickPlays.append(newKickPlay)
    currentId += 2

#Extracts only the punts
punts = selection(rawColumns, rawData, 'PlayType', 'PUNT')
for row in punts:
    playDescription = row[rawColumns['Description']]
    if "BLOCKED" in playDescription or "FUMBLE" in playDescription or "PENALTY" in playDescription or "(PUNT FORMATION)" in playDescription or "END GAME" in playDescription:
        continue
    playersInvolved = re.findall("\d*-[A-Z]\w*\.[A-Z]\w*", playDescription)
    yardage = re.findall("PUNTS [0-9]* YARDS", playDescription)[0].split(' ')[1]
    for i, p in enumerate(playersInvolved):
        if "'" in p:
            playersInvolved[i] = p.replaceAll("'", "")
    defenderId = None
    punterId = None
    goalScored = False
    if len(playersInvolved) >= 1:
        punterId = row[rawColumns['OffenseTeam']] + currentYear + playersInvolved[0]
    if punterId != None and punterId in players:
        gameId = getGameId(games, row[rawColumns['GameDate']], row[rawColumns['DefenseTeam']])
        newPlay = Play(currentId, gameId, formatId(defenderId), row[rawColumns['Quarter']], row[rawColumns['Minute']], row[rawColumns['Second']], yardage, 1 if goalScored else 0, "PUNT", currentId + 1)
        newPuntPlay = PuntPlay(currentId + 1, currentId, formatId(punterId))
        plays.append(newPlay)
        puntPlays.append(newPuntPlay)
    currentId += 2

#Extracts only the timeouts
timeoutPlays = selection(rawColumns, rawData, 'PlayType', 'TIMEOUT')
for row in timeoutPlays:
    gameId = getGameId(games, row[rawColumns['GameDate']], row[rawColumns['DefenseTeam']])
    newPlay = Play(currentId, gameId, 'NULL', row[rawColumns['Quarter']], row[rawColumns['Minute']], row[rawColumns['Second']], row[rawColumns['Yards']], 0, "TIMEOUT", currentId + 1)
    newTimeout = TimeOut(currentId + 1, currentId)
    plays.append(newPlay)
    timeouts.append(newTimeout)
    currentId += 2

coaches = []
coachesfors = []
for row in coachData:
    team = row[coachColumns['Team']]
    firstName = row[coachColumns['First']]
    lastName = row[coachColumns['Last']]
    teamId = team + str(currentYear)
    coachId = teamId + lastName
    coaches.append(Coach(formatId(coachId), firstName, lastName))
    coachesfors.append(CoachesFor(formatId(teamId), formatId(coachId), currentYear))

for team in teams:
    print("INSERT INTO Team (TeamId, City) VALUES ('{0}', '{1}');".format(team, teams[team]))

for game in games:
    print(game.getGameInsert())

for game in games:
    print(game.getParticipateInsert())

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

for p in puntPlays:
    print(p.getInsert())

for t in timeouts:
    print(t.getInsert())

for p in playsFors:
    print(p.getInsert())

for c in coaches:
    print(c.getInsert())

for cf in coachesfors:
    print(cf.getInsert())