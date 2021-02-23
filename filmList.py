import csv
import pandas as pd
import random

# 'status' should be SEEN or UNSEEN
def addFilm(name, status):
    filmList = open("filmList.csv", "a")
    filmList.write(f"\"{name}\",{status}\n")
    filmList.close()

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
        elif name in row[0]:
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

# Displays film staus if it exists in the list. 
def checkFilm(name):
    df = pd.read_csv("filmList.csv")
    for _, row in df.iterrows():
        if row["name"] == name:
            print("Name: ", row["name"], "\nStatus: ", row["status"])
            return
    print("Not in list...")

def menu():
    print("\n- SELECT OPERATION -")
    x = input("[rand, add, update, unseeen, check]: ")
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
    elif x == "update":
        name = input("\nEnter Name: ")
        updateFilm(name)
        print()
    elif x == "unseen":
        print("\nList of Unseen Films: ")
        showUnseen()
    elif x == "check":
        name = input("\nFilm to check: ")
        checkFilm(name)
    elif x == "q":
        print("\nQuitting program...")
        exit()
    else:
        print("\nInvalid Operation...")
    return menu()

if __name__ == "__main__":
    menu()