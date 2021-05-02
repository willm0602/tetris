import sqlite3
from constants import DB_PATH

def getConn(path = DB_PATH):
    conn = sqlite3.connect(path)
    return(conn)

def getScores():
    scoresQuery = execute("SELECT name, score FROM scores ORDER BY score desc;")
    return([score for score in scoresQuery])
    
def execute(query, params = []):
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    val = cursor.fetchall()
    cursor.close()
    conn.commit()
    return(val)

def addScore(name, score):
    execute("INSERT INTO scores VALUES (?, ?)",[name, score])
    