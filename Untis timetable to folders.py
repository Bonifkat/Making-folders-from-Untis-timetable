from datetime import datetime
from multiprocessing.sharedctypes import Value
from optparse import Values
import webuntis
import operator
import datetime
import os

s = webuntis.Session(
    server='',          #your schools server
    username='',        
    password='',
    school='',          #school name (from Untis)
    useragent=''        #not needed
)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

s.login()

today = datetime.date.today()

monday = today - datetime.timedelta(days=today.weekday())
tuesday = monday + datetime.timedelta(days=1)
wednesday = monday + datetime.timedelta(days=2)
thursday = monday + datetime.timedelta(days=3)
friday = monday + datetime.timedelta(days=4)

print(today.strftime("%A"))

if today.strftime("%A") == "Monday":
    timetable_day=monday
elif today.strftime("%A") == "Tuesday":
    timetable_day=tuesday
elif today.strftime("%A") == "Wednesday":
    timetable_day=wednesday
elif today.strftime("%A") == "Thursday":
    timetable_day=thursday
elif today.strftime("%A") == "Friday":
    timetable_day=friday
else:
    print("empty")

tt = s.timetable(klasse=3480, start=timetable_day, end=timetable_day)

# órák
block = []

for t in range(len(tt)):
    block.append({"start": tt[t]._data["startTime"], "end": tt[t]._data["endTime"]})
    block.sort(key=operator.itemgetter("start"))
    #print(block)
    # print(quick_sort(block))

sorrend = [None] * len(tt)

#print(len(tt))

for j in range(len(tt)):                #looping over every element in array "tt", looking at subjects one-by-one

    for i in range(len(tt)):            #looping over every element in array "tt", to get position of the subjects 
        if tt[j]._data["startTime"] == block[i]["start"]:

            allsu = s.subjects()

            for p in range(len(allsu)):
                if tt[j]._data["su"][0]["id"] == allsu[p]._data["id"]:

                    #print({j}, "class belongs to", {i}, "block", " |  " "subject: ", allsu[p]._data["name"])
                    #sorrend[i] =  {j}, "class belongs to", {i}, "block", " |  " "subject: ", allsu[p]._data["name"]
                    sorrend[i] =  i+1, " |  ", "subject: ", allsu[p]._data["longName"], allsu[p]._data["id"]

                    #creating folder
                    su_exceptions = ["", ""] # set subject which doesn't need it's own folder

                    if allsu[p]._data["name"] in su_exceptions:
                        pass
                    else:
                        createFolder(allsu[p]._data["name"] + '/' + allsu[p]._data["name"])

print(sorrend[i])
print("---------------------")
for k in range(len(sorrend)):
    print(*sorrend[k])

s.logout()
