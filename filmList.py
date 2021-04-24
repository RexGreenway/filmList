import pandas as pd
import csv
import random
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Google Drive Authorisation Process
gauth = GoogleAuth()
# Saves credentials locally for Authorisation
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

# Grabs details of filmList file in google drive.
file_list = drive.ListFile({"q" : "title='filmList.csv' and trashed=false"}).GetList()
filmList_id = file_list[0]["id"]
filmList = drive.CreateFile({"id" : filmList_id})
filmList.GetContentFile("filmList.csv")

# Film List functions
# 'status' should be SEEN or UNSEEN
def addFilm(name, status):
    filmList = open("filmList.csv", "a")
    filmList.write(f"\"{name}\",{status}\n")
    filmList.close()

def removeFilm(name):
    filmList_reader = open("filmList.csv", "r")
    csv_read = csv.reader(filmList_reader.readlines())
    csv_write = csv.writer(open("filmList.csv", "w", newline=""))
    state = False
    # Goes through each row in the csv
    for row in csv_read:
        # If an existing name is entered replace with the SEEN
        if name == row[0]:
            print("Film Removed")
            pass
            state = True
        # If name is close show possible reccomendations. Then write the row.
        elif name in row[0]:
            print("See also: ", row[0])
            csv_write.writerow(row)
        # Always write the row.
        else:
            csv_write.writerow(row)
    if state == False:
        print("No Such Film.")
    filmList_reader.close()

def randomUnseenFilm():
    df = pd.read_csv("filmList.csv")
    unseen_df = df.loc[df["status"] == "UNSEEN"]
    unseen_df = unseen_df.reindex()
    rand = random.randint(0, len(unseen_df.index) - 1)
    print(unseen_df.iloc[rand]["name"])

def updateFilm(name):
    filmList_reader = open("filmList.csv", "r")
    csv_read = csv.reader(filmList_reader.readlines())
    csv_write = csv.writer(open("filmList.csv", "w", newline=""))
    state = False
    # Goes through each row in the csv
    for row in csv_read:
        # If an existing name is entered replace with the SEEN
        if name == row[0]:
            print("Film Updated")
            csv_write.writerow([row[0], "SEEN"])
            state = True
        # If name is close show possible reccomendations. Then write the row.
        elif name.lower() in row[0].lower():
            print("See also: ", row[0])
            csv_write.writerow(row)
        # Always write the row.
        else:
            csv_write.writerow(row)
    if state == False:
        print("No Such Film.")
    filmList_reader.close()

# Prints just the name column.
def showUnseen():
    df = pd.read_csv("filmList.csv")
    unseen_df = df.loc[df["status"] == "UNSEEN", "name"]
    print(unseen_df.to_string(index=False))

def showSeen():
    df = pd.read_csv("filmList.csv")
    unseen_df = df.loc[df["status"] == "SEEN", "name"]
    print(unseen_df.to_string(index=False))

# Prints entire film list
def showAll():
    df = pd.read_csv("filmList.csv")
    print(df.to_string(index=False))

# Displays film staus if it exists in the list. 
def checkFilm(name):
    filmList_reader = open("filmList.csv", "r")
    csv_read = csv.reader(filmList_reader.readlines())
    csv_write = csv.writer(open("filmList.csv", "w", newline=""))
    state = False
    # Goes through each row in the csv
    for row in csv_read:
        # If an existing name is entered replace with the SEEN
        if name.lower() in row[0].lower():
                print("Films: ", row)
                state = True
        csv_write.writerow(row)
    if state == False:
        print("No Such Film.")
    filmList_reader.close()

def menu():
    print("\n- SELECT OPERATION -")
    x = input("[rand, add, remove, update, unseeen, seen, check, all]: ")
    if x == "rand":
        print("\nRandom Unseen Film: ")
        randomUnseenFilm()
    elif x == "add":
        name = input("\nEnter Name: ")
        status = input("Enter Status [SEEN, UNSEEN]: ")
        if status in ["SEEN", "UNSEEN"]:
            addFilm(name, status)
        else:
            print("\nStatus should be SEEN or UNSEEN...")
    elif x == "remove":
        name = input("\nEnter Name: ")
        removeFilm(name)
    elif x == "update":
        name = input("\nEnter Name: ")
        updateFilm(name)
        print()
    elif x == "unseen":
        print("\nList of Unseen Films: ")
        showUnseen()
    elif x == "seen":
        print("\nList of Seen Films: ")
        showSeen()
    elif x == "check":
        name = input("\nFilm to check: ")
        checkFilm(name)
    elif x == "all":
        print("\nList of All Films: ")
        showAll()
    elif x == "q":
        filmList.SetContentFile("filmList.csv")
        filmList.Upload()
        print("\nUpdated Film List and uploaded to drive. Quitting program...")
        exit()
    else:
        print("\nInvalid Operation...")
    return menu()

menu()