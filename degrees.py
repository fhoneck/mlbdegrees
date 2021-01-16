import streamlit as st
import pandas as pd
import random

h = pd.read_csv("hittersall.csv")
p = pd.read_csv("pitchersall.csv")
sheet = pd.concat([h,p])
sheet = sheet.drop_duplicates()
sheet = sheet[sheet["Team"] != "- - -"]
sheet["Team"] = sheet["Season"].astype(str) + " " + sheet["Team"]
sheet = sheet[["Name","Season","Team","playerid"]]

def teamsList(player):
    l = sheet[sheet["playerid"]==player]
    l = l.sort_values(by = "Season", ascending = False)
    return(list(l["Team"]))

def teammatesSheet(teams):
    return(sheet[sheet["Team"].isin(teams)])

def teammatesList(teams):
    l = list(set(list(sheet[sheet["Team"].isin(teams)]["playerid"])))
    random.shuffle(l)
    return(l)

def fastTeammatesList(teams,oldplayer,minimumjump):
    o = max(sheet[sheet["playerid"]==oldplayer]["Season"])
    l = list(set(list(sheet[sheet["Team"].isin(teams)]["playerid"])))
    newl = []
    for dude in l:
        if max(sheet[sheet["playerid"]==dude]["Season"]) - o >= minimumjump:
            newl.append(dude)
    random.shuffle(newl)
    return(newl)
    
def firstConnection(p1,p2):
    p1name = sheet[sheet["playerid"]==p1]["Name"].iloc[0]
    p2name = sheet[sheet["playerid"]==p2]["Name"].iloc[0]
    p1teams = teamsList(p1)
    teammates = teammatesSheet(p1teams)
    check = teammates[teammates["playerid"]==p2]
    return(str(p1name) + " played on the " + check.head(1)["Team"].iloc[0] + " with " + p2name)
                
def fastConnectionList(p1,p2,minimumjump):
    for cushion in range(0,1):
        #first
        p1teams = teamsList(p1)
        p1teammates = fastTeammatesList(p1teams,p1,minimumjump)
        first = []
        mybar.progress(0.05)
        myslot.text("Searching for 1st Connections")
        for i in p1teammates:
            this = [p1,i]
            if i == p2:
                mybar.progress(1.0)
                myslot.text("Done!")
                return(this)
            else:
                if len(this) == len(set(this)):
                    first.append(this)
        #second
        second = []
        mybar.progress(0.15)
        myslot.text("Searching for 2nd Connections")
        for x in first:
            p = x[1]
            p1teams = teamsList(p)
            p1teammates = fastTeammatesList(p1teams,p,minimumjump)
            for i in p1teammates:
                this = [p1,p,i]
                if i == p2:
                    mybar.progress(1.0)
                    myslot.text("Done!")
                    return(this)
                else:
                    if len(this) == len(set(this)):
                        second.append(this)
        #third
        third = []
        mybar.progress(0.3)
        myslot.text("Searching for 3rd Connections")
        for x in second:
            o = x[1]
            p = x[2]
            p1teams = teamsList(p)
            p1teammates = fastTeammatesList(p1teams,p,minimumjump)
            for i in p1teammates:
                this = [p1,o,p,i]
                if i == p2:
                    mybar.progress(1.0)
                    myslot.text("Done!")
                    return(this)
                else:
                    if len(this) == len(set(this)):
                        third.append(this)
        #fourth
        fourth = []
        mybar.progress(0.5)
        myslot.text("Searching for 4th Connections")
        for x in third:
            o = x[1]
            t = x[2]
            p = x[3]
            p1teams = teamsList(p)
            p1teammates = fastTeammatesList(p1teams,p,minimumjump)
            for i in p1teammates:
                this = [p1,o,t,p,i]
                if i == p2:
                    mybar.progress(1.0)
                    myslot.text("Done!")
                    return(this)
                else:
                    if len(this) == len(set(this)):
                        fourth.append(this)
        #fifth
        fifth = []
        mybar.progress(0.75)
        myslot.text("Searching for 5th Connections")
        for x in fourth:
            o = x[1]
            t = x[2]
            s = x[3]
            p = x[4]
            p1teams = teamsList(p)
            p1teammates = fastTeammatesList(p1teams,p,minimumjump)
            for i in p1teammates:
                this = [p1,o,t,s,p,i]
                if i == p2:
                    mybar.progress(1.0)
                    myslot.text("Done!")
                    return(this)
                else:
                    if len(this) == len(set(this)):
                        fifth.append(this)
        #sixth
        sixth = []
        mybar.progress(0.99)
        myslot.text("Searching for 6th Connections")
        for x in fifth:
            o = x[1]
            t = x[2]
            s = x[3]
            r = x[4]
            p = x[5]
            p1teams = fastTeamsList(cushion,p)
            p1teammates = fastTeammatesList(p1teams,p,minimumjump)
            for i in p1teammates:
                this = [p1,o,t,s,r,p,i]
                if i == p2:
                    mybar.progress(1.0)
                    myslot.text("Done!")
                    return(this)
                else:
                    if len(this) == len(set(this)):
                        sixth.append(this)
        
def resultList(l):
    p1name = sheet[sheet["playerid"]==p1]["Name"].iloc[0]
    p2name = sheet[sheet["playerid"]==p2]["Name"].iloc[0]
    p1debut = min(sheet[sheet["playerid"]==p1]["Season"])
    p2debut = min(sheet[sheet["playerid"]==p2]["Season"])
    p1last = max(sheet[sheet["playerid"]==p1]["Season"])
    p2last = max(sheet[sheet["playerid"]==p2]["Season"])
    st.write("Player 1: ", p1name, " | played in ", p1debut)
    st.write("Player 2: " + p2name + " | played in ",p2last)
    try:
        for i in range(0,len(l)-1):
            st.write(firstConnection(l[i],l[i+1]))
    except:
        st.write("Could not find a connection with these parameters.")

def playerList(search):
    fits = sheet[sheet["Name"].str.contains(search,na=False,case=False)]
    fits['Debut'] = (fits['playerid'].map(fits.groupby('playerid')['Season'].min()))
    fits["Last"]= (fits['playerid'].map(fits.groupby('playerid')['Season'].max()))
    fits["Years"] = fits["Debut"].astype(str) + "-" + fits["Last"].astype(str)
    fits = fits[["Name","playerid","Years"]]
    fits = fits.drop_duplicates()
    fits = fits.sort_values(by="Name")
    fits["combo"] = fits["Name"] + " " + fits["Years"] + " (" + fits["playerid"].astype(str) +")"
    return(list(fits["combo"]))

st.header("MLB Degrees of Separation")
cols = st.beta_columns(2)
p1search = cols[0].text_input("Player 1 Search")
p1list = playerList(p1search)
p1 = cols[1].selectbox("Player 1",p1list)
p1 = [p.split(')')[0] for p in p1.split('(') if ')' in p][0]

cols2 = st.beta_columns(2)
p2search = cols2[0].text_input("Player 2 Search")
p2list = playerList(p2search)
p2 = cols2[1].selectbox("Player 2",p2list)
p2 = [p.split(')')[0] for p in p2.split('(') if ')' in p][0]
minimumjump = st.slider("Shortcuts",0,20)
if minimumjump == 0:
    minimumjump = -100
st.write("A large Shortcuts number speeds up long searches, but risks missing connections. 0 is the slowest but most thorough search.")

if st.button("Run"):
    p1 = int(p1)
    p2 = int(p2)
    p1debut = min(sheet[sheet["playerid"]==p1]["Season"])
    p2debut = min(sheet[sheet["playerid"]==p2]["Season"])
    if p2debut < p1debut:
        p3 = p1
        p1 = p2
        p2 = p3
    mybar = st.progress(0)
    myslot = st.empty()
    resultList(fastConnectionList(p1,p2,minimumjump))