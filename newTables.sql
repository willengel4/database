drop table player;
drop table team;
drop table plays_for;
drop table coach;
drop table coaches_for;
drop table Participates_In;
drop table play;
drop table puntplay;
drop table passplay;
drop table RunPlay;
drop table KickPlay;
drop table TimeOut;
drop table Weather;

CREATE TABLE Player (
    PlayerID varchar(50) NOT NULL,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    PlayerNumber INT,
    Height NUMERIC(5,2),
    Weight NUMERIC(5,2),
    Speed NUMERIC(5,2),
    BirthDate DATE,
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
    EndDate DATE,
    StartDate DATE,
    Role VARCHAR(50),
    PlayerID INT NOT NULL,
    TeamID INT NOT NULL,
    CONSTRAINT plays_for_pk PRIMARY KEY (StartDate, PlayerID, TeamID),
    CONSTRAINT fk_player_for FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID),
CONSTRAINT fk_team_for FOREIGN KEY (TeamID) REFERENCES Team(TeamID));

CREATE TABLE Coach (
    CoachID VARCHAR(50) NOT NULL,
    HomeTown VARCHAR(50),
    Name VARCHAR(50),
CONSTRAINT coach_pk PRIMARY KEY (CoachID));

CREATE TABLE Coaches_For(
    StartDate DATE,
    EndDate DATE,
    TeamID INT NOT NULL,
    CoachID INT NOT NULL,
    CONSTRAINT coaches_for_pk PRIMARY KEY (StartDate, TeamID, CoachID),
    CONSTRAINT fk_coach_team FOREIGN KEY (TeamID) REFERENCES Team(TeamID),
CONSTRAINT fk_coach FOREIGN KEY (CoachID) REFERENCES Coach(CoachID));

CREATE TABLE Game (
    GameID VARCHAR(50) NOT NULL,
    City VARCHAR(50), 
    Game_Date DATE,
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
    Boolean INT,
    PlayType VARCHAR(50),
    PlayTypeID INT NOT NULL,
    DefenderID INT,
    GameID VARCHAR(50) NOT NULL,
    CONSTRAINT play_pk PRIMARY KEY (PlayID),
    CONSTRAINT play_fk_def FOREIGN KEY (DefenderID) REFERENCES Player(PlayerID),
CONSTRAINT play_fk_game FOREIGN KEY(GameID) REFERENCES Game(GameID));

CREATE TABLE PuntPlay(
    PuntID INT NOT NULL,
    PlayID INT NOT NULL,
    PunterID INT NOT NULL,
    CONSTRAINT punt_pk PRIMARY KEY (PuntID, PlayID),
    CONSTRAINT punt_fk_play FOREIGN KEY (PlayID) REFERENCES Play(PlayID),
CONSTRAINT punt_fk_player FOREIGN KEY (PunterID) REFERENCES Player(PlayerID));

CREATE TABLE PassPlay (
    PassID INT NOT NULL,
    PlayID INT NOT NULL,
    PasserID INT NOT NULL,
    ReceiverID INT,
    Completed BOOLEAN,
    CONSTRAINT pass_pk PRIMARY KEY (PassID, PlayID),
    CONSTRAINT pass_fk_play FOREIGN KEY (PlayID) REFERENCES Play(PlayID),
    CONSTRAINT pass_fk_player1 FOREIGN KEY (PasserID) REFERENCES Player(PlayerID),
CONSTRAINT pass_fk_player2 FOREIGN KEY(ReceiverID) REFERENCES Player(PlayerID));

CREATE TABLE RunPlay (
    RunID INT NOT NULL,
    PlayID INT NOT NULL,
    RunnerID INT NOT NULL,
    CONSTRAINT run_pk PRIMARY KEY (RunID, PlayID),
    CONSTRAINT run_fk_play FOREIGN KEY (PlayID) REFERENCES Play(PlayID),
CONSTRAINT run_fk_player FOREIGN KEY (RunnerID) REFERENCES Player(PlayerID));

CREATE TABLE KickPlay (
    KickID INT NOT NULL,
    PlayID INT NOT NULL,
    KickerID INT NOT NULL,
    CONSTRAINT kick_pk PRIMARY KEY (KickID, PlayID),
    CONSTRAINT kick_fk_play FOREIGN KEY (PlayID) REFERENCES Play(PlayID),
CONSTRAINT kick_fk_player FOREIGN KEY (KickerID) REFERENCES Player(PlayerID));

CREATE TABLE TimeOut (
    TimeOutID INT NOT NULL,
    Duration NUMERIC(5,2) NOT NULL,
    PlayID INT NOT NULL,
    CONSTRAINT timeout_pk PRIMARY KEY (TimeOutID, PlayID),
CONSTRAINT timeout_fk_play FOREIGN KEY (PlayID) REFERENCES Play(PlayID));

CREATE TABLE Weather (
    WeatherID INT NOT NULL,
    WeatherDate DATE,
    City VARCHAR(50),
    Windspeed NUMERIC(5,2),
    Precipitation NUMERIC(5,2),
    SeaLevelPressure NUMERIC(5,2),
    Temperature NUMERIC(5,2),
    GameID INT NOT NULL,
    CONSTRAINT weather_pk PRIMARY KEY (WeatherID),
CONSTRAINT weather_fk_game FOREIGN KEY (GameID) REFERENCES Game(GameID));