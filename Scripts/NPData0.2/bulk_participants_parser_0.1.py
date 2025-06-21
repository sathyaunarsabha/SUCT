from datetime import datetime
import pandas as pd
import glob

attendencethres = 50

csvcount = 0
for file_name in glob.iglob('./*.csv', recursive=True):
    csvcount += 1
    print(file_name)

if (csvcount == 0):
    print("ERROR: No CSV File found !")
else:
    print("%d CSV Files found !"%csvcount)

print ('Attendence threshold: %d'%attendencethres)

dict = {}
mattendence = {}
nattendence = {}

types_of_encoding = ["utf8", "cp1252", "utf-8"]
columnnames = ['Topic','Meeting ID','User Name','User Email','Department','Group','Zoom Room','Creation Time','Start Time','End Time','Meeting Duration','Participants',
                'Original Name','User Email','Join Time','Leave Time','User Duration','Guest','Recording Consent']

for file_name in glob.iglob('./*.csv', recursive=True):

    inpcsvfile = open(file_name, "r", encoding="utf-8")

    df = pd.read_csv(inpcsvfile) # , header=0, usecols=columnnames

    df.reset_index(drop=True, inplace=True)
    
    #print(list(df.columns))
    #print(df.head())

    #print(df[['Creation Time','Start Time', 'Participants', 'Leave Time']])

    df.rename(columns = {'Creation Time':'start', 'Start Time':'end', 'Participants':'name', 'Leave Time':'attendtime'}, inplace = True)

    #print(df[ ['start','end', 'name', 'attendtime'] ])
    
    #filtering those who are present for more than 30 minutes
    dfvalid1 = df[df['attendtime']>30] [['start','end', 'name', 'attendtime']]
    #print(dfvalid1)

    for ind in dfvalid1.index:
        #print(dfvalid1['start'][ind], dfvalid1['name'][ind], dfvalid1['end'][ind])
        #print(type(dfvalid1['start'][ind]))
        datetimeobj = datetime.strptime(dfvalid1['start'][ind], '%m/%d/%Y %H:%M:%S')
        
        morning = False
        if( datetimeobj.hour >= 4 and datetimeobj.hour < 7):
            #print ("Morning session")
            morning = True

        evening = False
        if( datetimeobj.hour >= 19 and datetimeobj.hour <= 21):
            #print ("Morning session")
            evening = True

        year = datetimeobj.year
        month = datetimeobj.month
        day = datetimeobj.day

        if morning:
            datestr = str(str(year)+str(month)+str(day)+'m')
        elif evening:
            datestr = str(str(year)+str(month)+str(day)+'n')

        name = dfvalid1['name'][ind]
        #check if the name has 'NP''Np''nP''np'
        if ('np' in name or 'NP' in name or 'Np' in name or 'nP' in name or 'N.P' in name or 'n.p' in name or 'N.p' in name or 'n.P' in name):
            #maintain a table for all names and update the count of attendence
            #take attendence for each unique name for that year, month, date, session
            if (name not in dict):
                dict[name] = list()
                dict[name].extend(datestr)
                if(morning):
                    mattendence[name] = int(1)
                if(evening):
                    nattendence[name] = int(1)
            else:
                #if attendence is already added, then do not count again
                if (datestr not in dict[name]):
                    dict[name].extend(datestr)
                if(morning):
                    if(name in mattendence):
                        mattendence[name] = mattendence[name] + 1
                    else:
                        mattendence[name] = 1
                if(evening):
                    if(name in nattendence):
                        nattendence[name] = nattendence[name] + 1
                    else:
                        nattendence[name] = 1
        #end of valid name if

    #end of looping all rows
#end of looping all CSV files

#loop all attendence data, and output as per the threshold set
#output morning and evening data separately
print('Morning regular Non pattarai:')
for key in dict:
    if (key in mattendence):
        if(mattendence[key] > attendencethres):
            print (key)
print('Evening regular Non pattarai:')
for key in dict:
    if (key in nattendence):
        if(nattendence[key] > attendencethres):
            print (key)

#print the total number of days of data parsed and total attendence for each day, session


    





'''
# field names
# fields = ['Name', 'Branch', 'Year', 'CGPA']

# data rows of csv file
# rows = [ ['Nikhil', 'COE', '2', '9.0'],
         ['Sanchit', 'COE', '2', '9.1'],
         ['Aditya', 'IT', '2', '9.3'],
         ['Sagar', 'SE', '1', '9.5'],
         ['Prateek', 'MCE', '3', '7.8'],
         ['Sahil', 'EP', '2', '9.1']]

# name of csv file
filename= "university_records.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter= csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)

    # csv.DictReader(inpcsvfile)
    # for row in zoomreader:
    #    print(row['Name (Original Name)'], row['Start Time'], row['Duration (Minutes)'])


# import os
# arr = os.listdir('.')
# print(arr)

'''