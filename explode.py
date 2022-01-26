import hashlib
import logging
#from random import random, randrange
import requests
import jmespath
import datetime
from datetime import datetime as dt
import time


def getstats(player):
    url = "https://api.nhle.com/stats/rest/en/skater/summary"

    querystring = {"isAggregate": "false", "isGame": "false",
                   "factCayenneExp": "gamesPlayed>=1",
                   "cayenneExp": "gameTypeId=2 and seasonId<=20212022 and seasonId>=20212022 and skaterFullName likeIgnoreCase \"%"+str(player)+"%\""}

    payload = ""
    time.sleep(1)
    response = requests.request("GET", url, data=payload, params=querystring).json()
    output = jmespath.search("data", response)[0]
    output_list = list(output.keys())


    return output

def roundnum(number):
    global outnumber
    try:
        val = int(number)
        outnumber = number
    except ValueError:
        try:
            val = float(number)
            outnumber = round(val, 1)
        except ValueError:
            print(number + " ::: No.. input is not a number. It's a string")
    return outnumber

def explode(player1, player2):
    statdict = {"gamesPlayed": "GP ",
        "assists": "A  ",
        "goals": "G  ",
        "points": "P  ", "evGoals": "evG", "evPoints": "evP",
        "ppGoals": "ppG",
        "ppPoints": "ppP", "shGoals": "shG",
        "shPoints": "shP",
        "otGoals": "otG", "gameWinningGoals": "gwG",
        "plusMinus": "+/-",
        "pointsPerGame": "P/G", "faceoffWinPct": "FO%",
        "shots": "SAT",
        "shootingPct": "SH%",
        "penaltyMinutes": "PIM",
        "timeOnIcePerGame": "TOI",
        "lastName": "Malkin",
        "playerId": 8471215,
        "positionCode": "POS",
        "seasonId": 20212022,
        "shootsCatches": "L",
        "skaterFullName": "Evgeni Malkin", "teamAbbrevs": "PIT"
    }

    statlist = ['gamesPlayed', 'assists', 'goals','points','evGoals','evPoints','ppGoals','ppPoints','shGoals','shPoints','otGoals','gameWinningGoals','plusMinus','pointsPerGame','faceoffWinPct','shots','shootingPct','penaltyMinutes','timeOnIcePerGame'           ]
    stat1 = getstats(player1)
    stat2 = getstats(player2)
    output = ""
    # print(stat1)
    print(stat1['lastName'] + " VS " + stat2['lastName'])
    output = '`' + stat1['lastName'] + " VS " + stat2['lastName'] + "\n--------------------`"
    for item in statlist:
        # print(statdict.get(item) + "   " + str(roundnum(str(stat1.get(item)))) + " : " + str(roundnum(str(stat2.get(item)))))
        output = output + "`\n" + statdict.get(item) + "   " + str(roundnum(str(stat1.get(item)))) + " : " + str(roundnum(str(stat2.get(item)))) + "`"
    #print(output)
    return output


def getquery():
    inputquery = input("Hello: ")
    output = str(inputquery).split(" ", 1)
    explode(output[0], output[1])

