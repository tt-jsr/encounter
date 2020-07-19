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

def SubtractHitPoints(cp, n):
    cp[current_hp] -= n

def PromptInt(prompt, default):
    ans = raw_input(prompt)
    try:
        return int(ans)
    except:
        return default

def Initiative():
    for c in GetPlayerList():
        n = PromptInt("{0}({1}): ".format(c[name], c[initiative]), None)
        if n:
            c[initiative] = n
    GetPlayerList().sort(reverse=True, key=InitiativeSortFunc)

def AddPlayer():
    cp = {}
    cp[name] = raw_input("Name: ")
    cp[max_hp] = PromptInt("Max hp: ", 0)
    cp[current_hp] = cp[max_hp]
    cp[initiative] = PromptInt("Initiative: ", 1)
    cp[ac] = PromptInt("AC: ", 0)
    root[players].append(cp)
    GetPlayerList().sort(reverse=True, key=InitiativeSortFunc)
    return cp

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
        print "    " + GetNote(c).replace('\n', '\n    ')
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

def SetCurrentPlayer(idx):
    cl = GetPlayerList()
    if idx < 0 or idx >= len(cl):
        print "Out of range"
        return
    root[current_player_idx] = idx
    return GetCurrentPlayer()

# Promps the user for a player and returns it
def SelectPlayer():
    cl = GetPlayerList()
    counter=1
    for c in cl:
        print "{0}. {1}".format(counter, c[name])
        counter += 1
    n = PromptInt("Enter=> ", None)
    try:
        return cl[n-1]
    except:
        return None

def AddNote(cp, msg):
    f = "{0}-notes.txt".format(cp[name])
    try:
        f = open(f, "a")
        f.write("{0}\n".format(msg))
        f.close()
    except:
        pass

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
    ShowPlayer(GetCurrentPlayer())

def ShowPlayer(cp):
    ClearScreen()
    CursorPos(1, 1)
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

def PlayerMenu(cp):
    while True:
        ShowPlayer(cp)
        print " e. Edit Player note"
        print " h. Hit"
        print "hp. Edit HP"
        print " m. Edit Max HP"
        print "ac. Edit AC"
        print " s. Select Player"
        print " q. quit"
        ans = raw_input("Enter=> ")
        if ans == "e":
            EditNote(cp)
        if ans =='h':
            hp = PromptInt("Hit points: ", None)
            if hp:
                SubtractHitPoints(cp, hp)
                AddNote(cp, "Round {0}: Hit for {1} points {2}/{3}".format(GetRound(), hp, cp[current_hp], cp[max_hp]))
        if ans == 'hp':
            new_hp = PromptInt("HP ({0}): ".format(cp[current_hp]), None)
            if new_hp:
                cp[current_hp] = new_hp
                AddNote(cp, "Round {0}: Current HP changed to {1}, {2}/{3}".format(GetRound(), cp[current_hp], cp[current_hp], cp[max_hp]))
        if ans == 'm':
            new_hp = PromptInt("Max HP ({0}): ".format(cp[max_hp]), None)
            if new_hp:
                cp[max_hp] = new_hp
                AddNote(cp, "Round {0}: Max HP changed to {1}".format(GetRound(), cp[max_hp]))
        if ans == 'ac':
            new_ac = PromptInt("AC ({0}): ".format(cp[ac]), None)
            if new_ac:
                cp[ac] = new_ac
                AddNote(cp, "Round {0}: AC changed to {1}".format(GetRound(), cp[ac]))
        if ans == 's':
            ncp = SelectPlayer()
            if ncp:
                cp = ncp

        if ans == 'q':
            Save()
            return

def Menu():
    Load()
    while True:
        ShowCurrentPlayer()
        print "n. Next player               i. Set initiative"
        print "e. Edit Note                ap. Add player"
        print "a. Show all players         cp. Set Current Player"
        print "s. Select player"
        print "q. quit"
        ans = raw_input("Enter=> ")
        if ans == "a":
            ShowAllPlayers()
        if ans == "s":
            cp = SelectPlayer()
            if cp:
                PlayerMenu(cp)
        if ans == "n":
            NextPlayer()
            Save()
        if ans == "e":
            cp = GetCurrentPlayer()
            EditNote(cp)
        if ans == "i":
            Initiative()
            Save()
        if ans == 'cp':
            cp = SelectPlayer();
            if cp:
                idx = root[players].index(cp)
                root[current_player_idx] = idx
        if ans == "ap":
            cp = AddPlayer()
            PlayerMenu(cp)


        if ans == 'q':
            Save()
            return

Menu()



