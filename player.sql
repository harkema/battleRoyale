create database playerDB;
use playerDB;

CREATE TABLE Player
(
	PersonalID INT NOT NULL AUTO_INCREMENT,
    PlayerName VARCHAR(30),
    Strength INT,
    Charisma INT,
    Intelligence INT,
    Dexterity INT,
    PRIMARY KEY (PersonalID)
);


describe Player;

SELECT * FROM Player;

SET SQL_SAFE_UPDATES=0;

DELETE FROM Player WHERE PersonalID=158;

DELETE FROM Death;

DELETE FROM Round;

ALTER TABLE Player ADD COLUMN Kills INT AFTER Dexterity;

ALTER TABLE Round ADD COLUMN BattleID INT FIRST;

ALTER TABLE Death ADD COLUMN BattleID INT FIRST;

ALTER TABLE Death ADD COLUMN RoundID INT AFTER BattleID;

SELECT * FROM Death;

SELECT * FROM Round;

SELECT * FROM History;

SELECT * FROM Death WHERE BattleID = 111;

Describe Round;

Describe History;

Drop Table History;

ALTER TABLE Player MODIFY COLUMN Kills INT NOT NULL DEFAULT 0;

ALTER TABLE Death CHANGE RoundID RoundNumber INT;

CHECKSUM TABLE Player;

Describe Death;
