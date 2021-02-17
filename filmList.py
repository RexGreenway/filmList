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
        # If an existing name is enetered replace with the SEEN
        if name == row[0]:
            print("Film Updated")
            csv_write.writerow([row[0], "SEEN"])
            state = True
        # If name is close or a typo show possible reccomendations. Then write the row.
        elif name in row[0]:
            print("See also: ", row[0])
            csv_write.writerow(row)
        # Always write the row.
        else:
            csv_write.writerow(row)
    if state == False:
        print("No Such Film.")
    filmList_reader.close()

