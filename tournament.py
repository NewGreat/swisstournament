#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random


# Just a shortcut function to make connections more readable
def connect():
    return psycopg2.connect("dbname=tournament")


# Must both empty the matches table and delete all match data
# from the players table
def deleteMatches():
    conn = None
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    c.execute("UPDATE players SET wins = 0, matches = 0;")
    conn.commit()
    conn.close()
    return


# Clears out the players table entirely
def deletePlayers():
    conn = None
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit()
    conn.close()
    return


# Returns a full count of rows in players table
def countPlayers():
    conn = None
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM players;")
    results = c.fetchall()[0][0]
    conn.close()
    return results


# Adds new player to players table, setting default data to zero
def registerPlayer(name):
    conn = None
    conn = connect()
    c = conn.cursor()
    # Note substitution method used to avoid SQL injection attacks
    query = "INSERT INTO players (name, wins, matches) VALUES (%s, 0, 0)"
    c.execute(query, (name,))
    conn.commit()
    conn.close()
    return


# Returns all players sorted by wins (most to
# least) and then matches (most to least)
def playerStandings():
    conn = None
    conn = connect()
    c = conn.cursor()
    query = "SELECT id, name, wins, matches " + \
            "FROM players ORDER BY wins DESC, matches DESC;"
    c.execute(query)
    results = c.fetchall()
    conn.commit()
    conn.close()
    return results


# Marks the outcome of a single match by adding a row to matches table
# and updating wins and matches columns in players table
def reportMatch(winner, loser):
    # Text of 3 queries
    matchOutcome = "INSERT INTO matches (winner, loser) VALUES ('%s', '%s');"
    winnerOutcome = "UPDATE players SET wins = wins + 1, " + \
                    "matches = matches + 1 WHERE id = '%s';"
    loserOutcome = "UPDATE players SET matches = " + \
                   "matches + 1 WHERE id = '%s';"
    conn = None
    conn = connect()
    c = conn.cursor()
    # Execution of 3 queries (note again method used to avoid SQL injection)
    c.execute(matchOutcome, (winner, loser))
    c.execute(winnerOutcome, (winner,))
    c.execute(loserOutcome, (loser,))
    conn.commit()
    conn.close()
    return


# Child fn to selectPlayer() to create random non-repetitive player numbers
def rando(assignedPlayers, numPlayers):
    player = random.randint(0, numPlayers - 1)
    # The below only triggers if player was already assigned
    if player in assignedPlayers:
        player = rando(assignedPlayers, numPlayers)
    return player


# Child fn to noRematch() to match up
# random players of equivalent standing
def selectPlayer(assignedPlayers, numPlayers, results):
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


# Child fn to playerAssignment() to prevent repeat matches
def noRematch(output, assignedPlayers, numPlayers, results):
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


# Child fn to swissPairings() that transforms player
# numbers to actual player id and name tuple pairups
def playerAssignment(results, numPlayers):
    output = []
    assignedPlayers = []
    while len(assignedPlayers) < numPlayers:  # Runs until all players assigned
        # Before adding player matchup to output, check to make sure players
        # have not already faced one another
        p1, p2 = noRematch(output, assignedPlayers, numPlayers, results)
        output.append(results[p1][0:2] + results[p2][0:2])
    return output


# Parent matchup fn that runs the query and
# runs playerAssignment() once per each match
def swissPairings():
    conn = None
    conn = connect()
    c = conn.cursor()
    query = "SELECT * FROM players ORDER BY wins DESC"
    c.execute(query)
    results = c.fetchall()
    numPlayers = len(results)  # To help remember what len(results) signifies
    #
    # The below commented section could be used to run playerAssignment once
    # per each expected round of matches
    #
    # currentRound = 1
    # while currentRound <= numPlayers/2: # Runs once per expected round
    #     output = playerAssignment(results, numPlayers)
    #     currentRound += 1
    conn.commit()
    conn.close()
    return playerAssignment(results, numPlayers)
