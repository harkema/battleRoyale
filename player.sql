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

DELETE FROM Player;

DELETE FROM Death;

DELETE FROM Round;

ALTER TABLE Player ADD COLUMN Kills INT AFTER Dexterity;

ALTER TABLE Round ADD COLUMN BattleID INT FIRST;

ALTER TABLE Death ADD COLUMN BattleID INT FIRST;

ALTER TABLE Death ADD COLUMN RoundID INT AFTER BattleID;

SELECT * FROM Death;

SELECT * FROM Round;

Describe Round;

ALTER TABLE Player MODIFY COLUMN Kills INT NOT NULL DEFAULT 0;

ALTER TABLE Death CHANGE RoundID RoundNumber INT;
