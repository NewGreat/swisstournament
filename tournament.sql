
-- Cascade database drop used to remove all children
DROP DATABASE IF EXISTS tournament CASCADE;
CREATE DATABASE tournament;

\c tournament;


DROP TABLE IF EXISTS players CASCADE;
CREATE TABLE players
(
id serial PRIMARY KEY,
name varchar(255),
wins integer,
matches integer
);


-- Note foreign keys within matches that reference players
DROP TABLE IF EXISTS matches CASCADE;
CREATE TABLE matches
(
id serial PRIMARY KEY,
winner integer references players (id),
loser integer references players (id)
);
