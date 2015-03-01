#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2
import bleach
import pprint

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from players")
    result = c.fetchall()
    return int(result[0][0])



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players(name) VALUES(%s)", (bleach.clean(name),))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    query = "select players.id, players.name, winner.winner, total.total from players left join (select players.id, count(winner) as winner from players left join matches on players.id = matches.winner group by players.id) as winner on players.id = winner.id left join (select players.id, count(players.id) as total from players join matches on (players.id = matches.winner or players.id = matches.loser) group by players.id) as total on players.id = total.id order by winner desc;"
    c.execute(query)
    query_result = c.fetchall()
    players = [[int(row[0]), str(row[1]), int(row[2]), newPlayerCheck(row[3])] for row in query_result]

    return players

def newPlayerCheck(player):
    """
    Newly registered players should have no matches or wins.
    """
    if player is None:
        return 0
    else: 
        return player


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO matches(winner, loser) VALUES(%s, %s)", (bleach.clean(winner), bleach.clean(loser), ))
    db.commit()
    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = [(record[0], record[1]) for record in playerStandings()]
    standing_left = standings[0::2]
    standing_right = standings[1::2]
    pairs = zip(standing_left, standing_right)
    players = [tuple(list(sum(pairing, ()))) for pairing in pairs]

    return players
