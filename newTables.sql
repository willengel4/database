CREATE TABLE Player (
    PlayerID varchar(50) NOT NULL,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    PlayerNumber INT,
    Height NUMERIC(5,2),
    Weight NUMERIC(5,2),
    Speed NUMERIC(5,2),
    BirthDate varchar(50),
    College VARCHAR(50),
    Hometown VARCHAR(50),
CONSTRAINT player_pk PRIMARY KEY (PlayerID));

CREATE TABLE Team (
    TeamID varchar(59) NOT NULL,
    TeamName VARCHAR(50),
    City VARCHAR(50),
    State VARCHAR(50),
CONSTRAINT team_pk PRIMARY KEY (TeamID));

CREATE TABLE Plays_For (
    PlayerID varchar(50) NOT NULL,
    TeamID varchar(50) NOT NULL,
    Year INT NOT NULL,
    Role VARCHAR(50),
    CONSTRAINT plays_for_pk PRIMARY KEY (PlayerID, TeamID),
    CONSTRAINT fk_player_for FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID),
CONSTRAINT fk_team_for FOREIGN KEY (TeamID) REFERENCES Team(TeamID));

CREATE TABLE Coach (
    CoachID VARCHAR(50) NOT NULL,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
CONSTRAINT coach_pk PRIMARY KEY (CoachID));

CREATE TABLE Coaches_For(
    Year int not null,
    TeamID varchar(50) NOT NULL,
    CoachID varchar(50) NOT NULL,
    CONSTRAINT coaches_for_pk PRIMARY KEY (TeamID, CoachID),
    CONSTRAINT fk_coach_team FOREIGN KEY (TeamID) REFERENCES Team(TeamID),
CONSTRAINT fk_coach FOREIGN KEY (CoachID) REFERENCES Coach(CoachID));

CREATE TABLE Game (
    GameID VARCHAR(50) NOT NULL,
    Game_Date_Time DATE,
    City VARCHAR(10), 
CONSTRAINT game_pk PRIMARY KEY (GameID));

CREATE TABLE Participates_In (
    HomeTeamID VARCHAR(50) NOT NULL,
    GameID VARCHAR(50) NOT NULL,
    AwayTeamID VARCHAR(50) NOT NULL,
    CONSTRAINT part_pk PRIMARY KEY (HomeTeamID, GameID, AwayTeamID),
    CONSTRAINT part_fk_team1 FOREIGN KEY (HomeTeamID) REFERENCES Team(TeamID),
    CONSTRAINT part_fk_game FOREIGN KEY (GameID) REFERENCES Game(GameID),
CONSTRAINT part_fk_team2 FOREIGN KEY (AwayTeamID) REFERENCES Team(TeamID));

CREATE TABLE Play(
    PlayID INT NOT NULL,
    Quarter NUMERIC(5,2),
    Minute NUMERIC(5,2),
    Second NUMERIC(5,2),
    Yards NUMERIC(5,2),
    GoalScored Int,
    PlayType VARCHAR(50),
    PlayTypeID INT,
    DefenderID varchar(50),
    GameID VARCHAR(50) NOT NULL,
    CONSTRAINT play_pk PRIMARY KEY (PlayID),
CONSTRAINT play_fk_game FOREIGN KEY(GameID) REFERENCES Game(GameID));

CREATE TABLE PuntPlay(
    PuntID INT NOT NULL,
    PlayID INT,
    PunterID varchar(50) NOT NULL,
    CONSTRAINT punt_pk PRIMARY KEY (PuntID, PlayID),
CONSTRAINT punt_fk_player FOREIGN KEY (PunterID) REFERENCES Player(PlayerID));

CREATE TABLE PassPlay (
    PassID INT NOT NULL,
    PlayID INT,
    PasserID varchar(50) NOT NULL,
    ReceiverID varchar(50),
    Completed Int,
    CONSTRAINT pass_pk PRIMARY KEY (PassID, PlayID),
    CONSTRAINT pass_fk_player1 FOREIGN KEY (PasserID) REFERENCES Player(PlayerID),
CONSTRAINT pass_fk_player2 FOREIGN KEY(ReceiverID) REFERENCES Player(PlayerID));

CREATE TABLE RunPlay (
    RunID INT NOT NULL,
    PlayID INT,
    RunnerID varchar(50) NOT NULL,
    CONSTRAINT run_pk PRIMARY KEY (RunID, PlayID),
CONSTRAINT run_fk_player FOREIGN KEY (RunnerID) REFERENCES Player(PlayerID));

CREATE TABLE KickPlay (
    KickID INT NOT NULL,
    PlayID INT,
    KickerID varchar(50) NOT NULL,
    CONSTRAINT kick_pk PRIMARY KEY (KickID, PlayID),
CONSTRAINT kick_fk_player FOREIGN KEY (KickerID) REFERENCES Player(PlayerID));

CREATE TABLE TimeOut (
    TimeOutID INT NOT NULL,
    Duration NUMERIC(5,2) NOT NULL,
    PlayID INT,
    CONSTRAINT timeout_pk PRIMARY KEY (TimeOutID, PlayID));

CREATE TABLE Weather (
    WeatherID INT NOT NULL,
    WeatherDate DATE,
    City VARCHAR(50),
    Windspeed NUMERIC(5,2),
    Precipitation NUMERIC(5,2),
    SeaLevelPressure NUMERIC(5,2),
    Temperature NUMERIC(5,2),
    GameID varchar(50) NOT NULL,
    CONSTRAINT weather_pk PRIMARY KEY (WeatherID),
CONSTRAINT weather_fk_game FOREIGN KEY (GameID) REFERENCES Game(GameID));