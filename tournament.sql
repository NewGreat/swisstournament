
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament;


DROP TABLE IF EXISTS players CASCADE;
CREATE TABLE players
(
id serial PRIMARY KEY,
name varchar(255)
);


DROP TABLE IF EXISTS matches CASCADE;
CREATE TABLE matches
(
id serial PRIMARY KEY,
winner integer references players (id),
loser integer references players (id)
);
