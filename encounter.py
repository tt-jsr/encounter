#! /usr/bin/python
import json
import os
import sys

current_round="current_round"
current_player_idx="current_player_idx"
players="players"
max_hp="max-hp"
ac="ac"
initiative="initiative"
current_hp="current-hp"
name="name"
properties="properties"
url="url"
time="time"

root={
current_round:0,
current_player_idx:0,
time:0,
players:[
    {
        name:"Dimble",
        max_hp:39,
        ac:17,
        initiative:0,
        current_hp:39,
        url:"https://www.dndbeyond.com/profile/dimbledoorknocker/characters/13673198"
    },
    {
        name:"Talia",
        max_hp:42,
        ac:16,
        initiative:0,
        current_hp:42
    },
    {
        name:"Caleth",
        max_hp:0,
        ac:0,
        initiative:0,
        current_hp:0
    },
    {
        name:"Clarion",
        max_hp:59,
        ac:18,
        initiative:0,
        current_hp:59,
        url:"https://www.dndbeyond.com/profile/dimbledoorknocker/characters/14012702"
    },
    {
        name:"Shadow",
        max_hp:41,
        ac:16,
        initiative:0,
        current_hp:41
    },
    {
        name:"Knack",
        max_hp:45,
        ac:13,
        initiative:0,
        current_hp:45,
        url:"https://www.dndbeyond.com/profile/dimbledoorknocker/characters/14021635"
    },
    {
        name:"Rhien",
        max_hp:36,
        ac:17,
        initiative:0,
        current_hp:36,
        url:"https://www.dndbeyond.com/profile/dimbledoorknocker/characters/13672695"
    },
    {
        name:"Merishew",
        max_hp:51,
        ac:15,
        initiative:0,
        current_hp:51,
        url:"https://www.dndbeyond.com/profile/dimbledoorknocker/characters/14126880"
    },
    {
        name:"Failtask",
        max_hp:84,
        ac:15,
        initiative:0,
        current_hp:84,
        url:"https://www.dndbeyond.com/profile/dimbledoorknocker/characters/14172769"
    },
    {
        name:"Mage",
        max_hp:40,
        ac:12,
        initiative:0,
        current_hp:40,
        url:"https://www.dndbeyond.com/monsters/mage"
    },
    {
        name:"Archer1",
        max_hp:73,
        ac:16,
        initiative:0,
        current_hp:73,
        url:"https://www.dndbeyond.com/monsters/archer"
    },
    {
        name:"Archer2",
        max_hp:83,
        ac:16,
        initiative:0,
        current_hp:83,
        url:"https://www.dndbeyond.com/monsters/archer"
    },
    {
        name:"Archer3",
        max_hp:71,
        ac:16,
        initiative:0,
        current_hp:71,
        url:"https://www.dndbeyond.com/monsters/archer"
    },
    {
        name:"Dragon",
        max_hp:110,
        ac:17,
        initiative:0,
        current_hp:110,
        url:"https://www.dndbeyond.com/monsters/young-brass-dragon"
    }
]
}

def InitiativeSortFunc(c):
    return c[initiative]

def ClearScreen():
    sys.stdout.write("\033[2J")

def CursorPos(x, y):
    sys.stdout.write("\033[{0};{1}H".format(x, y))

def Save():
    s =json.dumps(root, sort_keys=True, indent=4, separators=(',', ': '))
    f = open("encounter.dat", "w")
    f.write(s)
    f.close()

def Load():
    global root
    f = open("encounter.dat", "r")
    s = f.read()
    root = json.loads(s)
    f.close()

def GetRound():
    return root[current_round]

def IncRound():
    root[current_round] += 1
    root[time] += 6

def GetPlayerList():
    return root[players]

def GetCurrentPlayer():
    idx = root[current_player_idx]
    return GetPlayerList()[idx]

def SubtractHitPoints(n):
    cp = GetCurrentPlayer()
    cp[current_hp] -= n

def Initiative():
    for c in GetPlayerList():
        ans = raw_input("{0}({1}): ".format(c[name], c[initiative]))
        try:
            n = int(ans)
            c[initiative] = n
        except:
            pass
    GetPlayerList().sort(reverse=True, key=InitiativeSortFunc)

def ShowAllPlayers():
    ClearScreen()
    CursorPos(1, 1)
    cl = GetPlayerList()
    cp = GetCurrentPlayer()
    for c in cl:
        percent = 0
        if c[max_hp] != 0:
            percent = int(float(c[current_hp])/float(c[max_hp])*100.0)
        star = ""
        if cp == c:
            star="*"
        print "{6}{0} ac={1} hp:{2}/{3} {4}% init:{5}".format(c[name], c[ac], c[current_hp], c[max_hp], percent, c[initiative], star)
        print GetNote(c)
    raw_input()

def NextPlayer():
    idx = root[current_player_idx]
    idx += 1
    cl = GetPlayerList()
    if idx == len(cl):
        IncRound()
        idx = 0
    root[current_player_idx] = idx
    return GetCurrentPlayer()

# Promps the user for a player and returns it
def SelectPlayer():
    cl = GetPlayerList()
    counter=1
    for c in cl:
        print "{0}. {1}".format(counter, c[name])
        counter += 1
    ans = raw_input("Enter=> ")
    try:
        n = int(ans)
        return cl[n-1]
    except:
        return None


def EditNote(cp):
    path = "vim {0}-notes.txt".format(cp[name])
    f = "{0}-notes.txt".format(cp[name])
    try:
        f = open(f, "a")
        f.write("Round {0}: \n".format(GetRound()))
        f.close()
    except:
        pass
    os.system(path)

def GetNote(cp):
    f = "{0}-notes.txt".format(cp[name])
    s = ""
    try:
        f = open(f, "r")
        s = f.read()
        f.close()
    except:
        pass
    return s

def ShowCurrentPlayer():
    ClearScreen()
    CursorPos(1, 1)
    cp = GetCurrentPlayer()
    cl = GetPlayerList()
    pos = "{0}/{1}".format(root[current_player_idx]+1, len(cl))
    percent = 0
    if cp[max_hp] != 0:
        percent = int(float(cp[current_hp])/float(cp[max_hp])*100.0)
    print """Round: {4} time: {7} {6}secs
Name:{0}
ac:{1}
hp:{3}/{2} {5}%\n""".format(cp[name], cp[ac], cp[max_hp],cp[current_hp], GetRound(), percent, root[time], pos)
    s = GetNote(cp)
    print s
    print
    print

def Menu():
    Load()
    ShowCurrentPlayer()
    while True:
        print "c. Current player"
        print "n. Next player"
        print "h. Hit"
        print "e. Edit Note"
        print "E. Edit Player note"
        print "a. Show all players"
        print "i. Initiative"
        print "u. Open webpage"
        #print "l. Load"
        print "q. quit"
        print "Enter=> "
        ans = raw_input()
        if ans == "c":
            ShowCurrentPlayer()
        if ans == "a":
            ShowAllPlayers()
            ShowCurrentPlayer()
        if ans == "n":
            NextPlayer()
            Save()
            ShowCurrentPlayer()
        if ans == "h":
            hp = raw_input("Hit points: ")
            if hp != "" and hp != '\n':
                SubtractHitPoints(int(hp))
            ShowCurrentPlayer()
        if ans == "e":
            cp = GetCurrentPlayer()
            EditNote(cp)
            ShowCurrentPlayer()
        if ans == "E":
            cp = SelectPlayer()
            if cp:
                EditNote(cp)
            ShowCurrentPlayer()
        if ans == "u":
            try:
                cp = GetCurrentPlayer()
                os.system("/mnt/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe " + cp[url])
            except:
                pass
            ShowCurrentPlayer()
        if ans == "i":
            Initiative()
            Save()
        if ans == 'q':
            Save()
            return

Menu()



