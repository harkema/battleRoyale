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