#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import contextmanager
import random


def connect():
    """Connect to the PostgreSQL database. Return a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except:
        print "Connection to PSQL database 'tournament' has failed. Sorry!"


@contextmanager
def getCursor():
    """Query helper function using contextlib. Creates a cursor from a
    database connection object, and performs queries using that cursor.
    """
    conn = None
    conn = connect()
    c = conn.cursor()
    try:
        yield c
    except:
        raise
    else:
        conn.commit()
    finally:
        c.close()
        conn.close()


def fullQuery():
    """Return a string to shorten query executions"""
    query = """SELECT
            players.id,
            players.name,
            COUNT(m1.winner) AS wins,
            (SELECT
                COUNT(m1.winner) + COUNT(m2.loser)) AS matches_played
        FROM players
            LEFT JOIN matches AS m1
                ON players.id = m1.winner
            LEFT JOIN matches AS m2
                ON players.id = m2.loser
        GROUP BY players.id
        ORDER BY players.id;
        """
    return query


def deleteMatches():
    """Remove all the match records from the database."""
    with getCursor() as cursor:
        cursor.execute("DELETE FROM matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    with getCursor() as cursor:
        cursor.execute("DELETE FROM players;")


def countPlayers():
    """Return the number of players currently registered."""
    with getCursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM players;")
        results = cursor.fetchall()[0][0]
    return results


def registerPlayer(name):
    """Add a player to the tournament database.

    The database assigns a unique serial id number for the player.

    Args:
        name: the player's full name (need not be unique).
    """
    with getCursor() as cursor:
        cursor.execute("INSERT INTO players (name) VALUES (%s);", (name,))


def playerStandings():
    """Return a list of the players and their win records, sorted by wins
    (most to least) and then matches (most to least).

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Return:
        A list of tuples, each of which contains (id, name, wins, matches):
            id: the player's unique id (assigned by the database)
            name: the player's full name (as registered)
            wins: the number of matches the player has won
            matches: the number of matches the player has played
    """
    with getCursor() as cursor:
        cursor.execute(fullQuery())
        results = cursor.fetchall()
    return results


def reportMatch(winner, loser):
    """Record the outcome of a single match between two players by adding a
    row to matches table and updating wins and matches columns in players
    table.

    Args:
        winner: the id number of the player who won
        loser: the id number of the player who lost
    """
    with getCursor() as cursor:
        query = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
        cursor.execute(query, (winner, loser))


def rando(assignedPlayers, numPlayers):
    """Return a number later used to make a player matchup.

    This function is fully subordinate to selectPlayer().

    Args:
        assignedPlayers: list of integers representing booked players
        numPlayers: integer representing count of players in tournament

    Return:
        player: a random, non-repetitive integer limited by numPlayers
    """
    player = random.randint(0, numPlayers - 1)
    # The below only triggers if player was already assigned
    if player in assignedPlayers:
        player = rando(assignedPlayers, numPlayers)
    return player


def selectPlayer(assignedPlayers, numPlayers, results):
    """Return a potential player matchup of equivalent standing.

    This function is fully subordinate to noRematch().

    Args:
        assignedPlayers: list of integers representing booked players
        numPlayers: integer representing count of players in tournament
        results: table used to extract player wins for equivalence comparison

    Return:
        p1: a random, non-repetitive integer limited by numPlayers
        p2: a random, non-repetitive integer limited by numPlayers
    """
    # Picking Player1 is easy
    p1 = rando(assignedPlayers, numPlayers)
    assignedPlayers.append(p1)
    # But Player2 needs to make sure to have equivalent wins
    # AND must not already be booked for a match
    p2 = rando(assignedPlayers, numPlayers)
    # The below loop only triggers if player wins not equivalent
    while results[p1][2] != results[p2][2]:
        p2 = rando(assignedPlayers, numPlayers)
    assignedPlayers.append(p2)
    return p1, p2


def noRematch(output, assignedPlayers, numPlayers, results):
    """Prevent repeat matches.

    This function is fully subordinate to playerAssignment().

    Args:
        output: list of tuples containing actual id and name for p1 and p2
        assignedPlayers: list of integers representing booked players
        numPlayers: integer representing count of players in tournament
        results: table used to extract player wins for equivalence comparison

    Return:
        p1: a confirmed player choice for a non-repetitive matchup with p2
        p2: a confirmed player choice for a non-repetitive matchup with p1
    """
    # Get a tentative p1 and p2 using child functions
    p1, p2 = selectPlayer(assignedPlayers, numPlayers, results)
    for matchup in output:
        # For a given tuple list item currently in the output...
        # 1) Check if the first player in that tuple is our current p1
        while results[p1][0] == matchup[0]:
            # 2) If so, check if p2 id already recorded
            while results[p2][0] == matchup[2]:
                # 3) If so, then this is a repeat matchup. That's bad!
                # So re-select players until we have a fresh match
                p1, p2 = selectPlayer(assignedPlayers, numPlayers, results)
        # Because players randomly assigned, must do same check w/second half
        # of the tuple list item, in case a duplicate exists in reverse
        while results[p1][0] == matchup[2]:
            while results[p2][0] == matchup[0]:
                p1, p2 = selectPlayer(assignedPlayers, numPlayers, results)
    return p1, p2


def playerAssignment(results, numPlayers):
    """Convert player integer assignments to actual id/name matchups.

    This function is fully subordinate to swissPairings().

    Args:
        assignedPlayers: list of integers representing booked players
        numPlayers: integer representing count of players in tournament

    Return:
        output: list of tuples containing actual id and name for p1 and p2
    """
    output = []
    assignedPlayers = []
    while len(assignedPlayers) < numPlayers:  # Runs until all players assigned
        # Before adding player matchup to output, check to make sure players
        # have not already faced one another
        p1, p2 = noRematch(output, assignedPlayers, numPlayers, results)
        output.append(results[p1][0:2] + results[p2][0:2])
    return output


def swissPairings():
    """Return a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings. Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Return:
        A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
    """
    with getCursor() as cursor:
        # Main query to get a table with id, name, wins, and matches
        cursor.execute(fullQuery())
        results = cursor.fetchall()
        # Separate query just to get a player count
        numPlayers = countPlayers()
    return playerAssignment(results, numPlayers)
