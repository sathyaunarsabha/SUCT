import csv
import re
from datetime import datetime
import pandas as pd
import glob

###### Inputs #######
NP_MAX_ID = 500
attendencethres = 50

#Atleast one session a day is considered as attendence for that
combine_mor_eve = False 



csvcount = 0
for file_name in glob.iglob('./*.csv', recursive=True):
    csvcount += 1
    print(file_name)

if (csvcount == 0):
    print("ERROR: No CSV File found !")
else:
    print("%d CSV Files found !"%csvcount)

print ('Attendence threshold: %d'%attendencethres)
if combine_mor_eve:
    print ('Combining morning and evening session data!')

days = {}
dict = {}
mattendence = {}
nattendence = {}
combattendence = {}
names = {}

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
    dfvalid1 = df[df['attendtime']>20] [['start','end', 'name', 'attendtime']]
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

        if not morning and not evening:
            continue

        year = datetimeobj.year
        month = datetimeobj.month
        day = datetimeobj.day

        if combine_mor_eve:
            datestr = str(str(year)+str(month)+str(day))
        else:
            if morning:
                datestr = str(str(year)+str(month)+str(day)+'m')
            elif evening:
                datestr = str(str(year)+str(month)+str(day)+'n')

        name = dfvalid1['name'][ind]
        #check if the name has 'NP''Np''nP''np'
        if ('np' in name or 'NP' in name or 'Np' in name or 'nP' in name or 'N.P' in name or 'n.p' in name or 'N.p' in name or 'n.P' in name):
            #maintain a table for all names and update the count of attendence
            #take attendence for each unique name for that year, month, date, session
            if datestr not in days:
                days[datestr] = 0
            days[datestr] = days[datestr] + 1

            #Valid ID
            validID = 1000
            numbers = re.findall(r'\d+', name)
            if len(numbers) != 0:
                for id in (numbers):
                    if int(id) < NP_MAX_ID:
                        validID = id
                        break
            else:
                #ID number is not mentioned in name
                continue
            
            #ID number is greater than 500
            if validID == 1000:
                continue

            #check = name            
            #ID based check instaead of Name
            check = validID
            if check not in names:
                names[check] = list()
            if name not in names[check]:
                names[check].append(str(name))
            
            if (check not in dict):
                dict[check] = list()
                dict[check].append(str(datestr))
                
                if combine_mor_eve:
                    combattendence[check] = int(1)
                else:
                    if(morning):
                        mattendence[check] = int(1)
                    if(evening):
                        nattendence[check] = int(1)
            else:
                #if attendence is already added, then do not count again
                if (datestr not in dict[check]):
                    dict[check].append(str(datestr))
                
                    if combine_mor_eve:
                        if (check not in combattendence):
                            raise "Error: Name not in combined attendence"
                        combattendence[check] = combattendence[check] + 1
                    else:
                        if(morning):
                            if(check in mattendence):
                                mattendence[check] = mattendence[check] + 1
                            else:
                                mattendence[check] = 1
                        if(evening):
                            if(check in nattendence):
                                nattendence[check] = nattendence[check] + 1
                            else:
                                nattendence[check] = 1
                #Data and session check
        #end of valid name if

    #end of looping all rows
#end of looping all CSV files



#loop all attendence data, and output as per the threshold set
if combine_mor_eve:
    npdatafile = open('.\\Output\\npdata_raw_combined.csv', mode='w', encoding="utf-8")
else:
    npdatafile = open('.\\Output\\npdata_raw_separate.csv', mode='w', encoding="utf-8")
npdatawriter = csv.writer(npdatafile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

if combine_mor_eve:
    npdatafilefilter = open('.\\Output\\npdata_final.csv', mode='w', encoding="utf-8")

    npdatawriterfilter = csv.writer(npdatafilefilter, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
else:
    npdatafilefilterm = open('.\\Output\\npdata_finalm.csv', mode='w', encoding="utf-8")
    npdatafilefiltern = open('.\\Output\\npdata_finaln.csv', mode='w', encoding="utf-8")

    npdatawriterfilterm = csv.writer(npdatafilefilterm, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    npdatawriterfiltern = csv.writer(npdatafilefiltern, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    npdatafilefiltermn = open('.\\Output\\npdata_finalboth_mn.csv', mode='w', encoding="utf-8")
    npdatawriterfiltermn = csv.writer(npdatafilefiltermn, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


if combine_mor_eve:
    for key in dict:
        if (key in combattendence):
            npdatawriter.writerow([str("".join(names[key][0])), combattendence[key]])

            if(combattendence[key] > attendencethres):
                print (names[key])
                #Write one name used by them
                npdatawriterfilter.writerow([str("".join(names[key][0])), combattendence[key]])
else:
    #output morning and evening data separately, both morning and evening data as well.

    print('Morning regular Non pattarai:')
    for key in dict:
        if (key in mattendence):
            npdatawriter.writerow([str("".join(names[key])), mattendence[key]])

            if(mattendence[key] > attendencethres):
                print (names[key])
                #Write one name used by them
                npdatawriterfilterm.writerow([str("".join(names[key][0])), mattendence[key]])
    print('Evening regular Non pattarai:')
    for key in dict:
        if (key in nattendence):
            npdatawriter.writerow([str("".join(names[key])), nattendence[key]])

            if(nattendence[key] > attendencethres):
                print (names[key])
                #Write one name used by them
                npdatawriterfiltern.writerow([str("".join(names[key][0])), nattendence[key]])

    print('Both Morning and Evening regular Non pattarai:')
    for key in dict:
        if (key in mattendence and key in nattendence):
            if(mattendence[key] > attendencethres and nattendence[key] > attendencethres):
                print (names[key])
                #Write one name used by them
                npdatawriterfiltermn.writerow([str("".join(names[key][0])), max(mattendence[key] , nattendence[key])])

print("Total number of days: %d"%len(days))
print("Attendence per day (Morning and Evening are both counted):")
for day in days:
    print("Day : %s "%day)
    print("Total Attendence: %d"%days[day])

'''
data = {'name': ['Somu', 'Kiku', 'Amol', 'Lini'],
	'physics': [68, 74, 77, 78],
	'chemistry': [84, 56, 73, 69],
	'algebra': [78, 88, 82, 87]}

	
#create dataframe
df_marks = pd.DataFrame(data)
print('Original DataFrame\n------------------')
print(df_marks)

new_row = {'name':'Geo', 'physics':87, 'chemistry':92, 'algebra':97}
#append row to the dataframe
df_marks = df_marks.append(new_row, ignore_index=True)
'''


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