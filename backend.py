import psycopg2
import requests
from time import sleep

def connect():
    conn = psycopg2.connect("dbname=thecellar user=root password=cdc host=localhost")


def addUser(userName, password, fName, lName):
    conn = psycopg2.connect("dbname=thecellar user=cdc password=cdc host=localhost")
    cur = conn.cursor()

    check = "SELECT EXISTS (SELECT 1 FROM USERS WHERE UNAME = '{}');".format(userName)
    cur.execute(check)
    result = cur.fetchone()[0]

    # return false if user exists
    if result:
        return False

    command = "INSERT INTO USERS (UNAME, PASS, FNAME, LNAME) VALUES ('{}','{}','{}','{}')".format(
        userName, password, fName, lName)
    print("Insert user command: {}".format(command))
    cur.execute(command)
    conn.commit()
    cur.close()
    conn.close()
    return True

def checkPassword(email, password):
    print("Starting check password")
    conn = psycopg2.connect("dbname=thecellar user=cdc password=cdc  host=localhost")  # TODO Convert back to localhost
    cur = conn.cursor()

    check = "SELECT EXISTS (SELECT 1 FROM users WHERE uname = '{}');".format(email)
    print(check)
    cur.execute(check)
    result = cur.fetchone()[0]

    print(result)
    # return false if user exists
    if not result:
        print("User not found")
        return False

    command = "SELECT pass FROM users WHERE uname = '{}';".format(email)
    print(command)
    cur.execute(command)
    correctPass = cur.fetchone()
    cur.close()
    conn.close()

    print("User: {} Psql: {}".format(password, correctPass))
    if password == correctPass[0]:
        print("And all is right with the world")
        return True
    else:
        print('All is dispair once again')
        return False


def userForEmail(email):
    conn = psycopg2.connect("dbname=thecellar user=cdc password=cdc host=localhost")
    cur = conn.cursor()
    command = "SELECT UNAME FROM USERS WHERE UNAME = '{}';".format(email)
    cur.execute(command)
    username = cur.fetchone()
    cur.close()
    conn.close()
    return username[0]

def currentState():
    conn = psycopg2.connect("dbname=thecellar user=cdc password=cdc host=localhost")
    cur = conn.cursor()
     
    cdn = "SELECT state,key FROM states WHERE key = 'northdoor' OR key = 'southdoor' OR key = 'westdoor' OR key = 'eastdoor' OR key = 'northhall' OR key = 'easthall' OR key = 'westhall' OR key = 'southhall';"

    #cdn = "select * from states;" 
    print(cdn)
    output = []
    print(output)
    cur.execute(cdn)
    #sleep(1)
    output = cur.fetchall()
    cur.close()
    conn.close()
 
    #might need this
    print( output)

    out = ['','','','','','','','']

    for i in range(0,8):
        if output[i][1] == 'northdoor':
            out[0] = output[i][0]
        if output[i][1] == 'southdoor':
            out[1] = output[i][0]
        if output[i][1] == 'eastdoor':
            out[2] = output[i][0]
        if output[i][1] == 'westdoor':
            out[3] = output[i][0]
        if output[i][1] == 'northhall':
            out[4] = output[i][0]
        if output[i][1] == 'southhall':
            out[5] = output[i][0]
        if output[i][1] == 'easthall':
            out[6] = output[i][0]
        if output[i][1] == 'westhall':
            out[7] = output[i][0]

    print(out)

    return out

def do(dir):
    conn = psycopg2.connect("dbname=thecellar user=cdc password=cdc host=localhost")
    cur = conn.cursor()

    check = "SELECT STATE FROM STATES WHERE KEY = '" + dir + "door';"
    print(check)
    cur.execute(check)
    state = cur.fetchone()

    print("State is")
    print(state)
       
    if state[0] == "0":
        print("its a zero")
        command = "UPDATE STATES SET STATE = '1' WHERE KEY = '" + dir + "door';"

    elif state[0] == "1":
        print("its a one")
        command = "UPDATE STATES SET STATE = '0' WHERE KEY = '" + dir + "door';"

    print(command)
    cur.execute(command)

    ncheck = "SELECT STATE FROM STATES WHERE KEY = '" + dir + "door';"
    cur.execute(ncheck)
    
    nstate = cur.fetchone()
    print("Old state {state[0]}, new state {nstate[0]}")
    print(nstate)
    conn.commit()
    cur.close()
    conn.close()
    return True
    
def ha(dir):
    conn = psycopg2.connect("dbname=thecellar user=cdc password=cdc host=localhost")
    cur = conn.cursor()

    check = "SELECT STATE FROM STATES WHERE KEY = '" + dir + "hall';"
    print(check)
    cur.execute(check)
    state = cur.fetchone()

    print("State is")
    print(state)
       
    if state[0] == "0":
        print("its a zero")
        command = "UPDATE STATES SET STATE = '1' WHERE KEY = '" + dir + "hall';"

    elif state[0] == "1":
        print("its a one")
        command = "UPDATE STATES SET STATE = '0' WHERE KEY = '" + dir + "hall';"

    print(command)
    cur.execute(command)

    ncheck = "SELECT STATE FROM STATES WHERE KEY = '" + dir + "hall';"
    cur.execute(ncheck)
    
    nstate = cur.fetchone()
    print("Old state {state[0]}, new state {nstate[0]}")
    print(nstate)
    conn.commit()
    cur.close()
    conn.close()
    return True
    



