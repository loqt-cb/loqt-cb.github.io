

''' 
Hello, 
This is a CSV parser for Windows Event Logs that provides information about each event that occurs.

Made by loqt-cb on Github.
'''
import csv

csv_in = "sec2.csv"
checked = []
fields = []
rows = []

'''
RecordNumber    0
EventRecordId   1
TimeCreated     2
EventId         3
Level           4
Provider        5
Channel         6
ProcessId       7
ThreadId        8
Computer        9
ChunkNumber     10
UserId          11
MapDescription  12
UserName        13
RemoteHost      14
PayloadData1    15
PayloadData2    16
PayloadData3    17
PayloadData4    18
PayloadData5    19
PayloadData6    20
ExecutableInfo  21
HiddenRecord    22
SourceFile      23
Keywords        24
ExtraDataOffset 25
Payload         26
'''

with open(f'{csv_in}', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)

    print("Total no. of rows: %d" % csvreader.line_num)

print('Field names are: ' + ", ".join(fields))

'''
print('\nFirst 5 rows are: \n')
for row in rows[:5]:
    for col in row:
        print(col)
'''

print("\nEventIds are: ")

for row in rows:
    for col in row:
        if col == row[3]:
            event_id = int(col)
            if event_id == 4688:
                # process creation
                print("\n\tID 4688: - A new process was created - ")
                print(f"Creator name: {row[13]}")

            elif event_id == 4672:
                # potential admin access on logon
                print("\n\tID 4672: - A special logon was detected - ")
                print(f"User name: {row[13]}")
            
            elif event_id == 4720:
                # account created
                print("\n\tID 4720: - A user account was created - ")
                print(f"\tUsername: {row[13]}")
                print(f"\tUser ID: {row[11]}")
            
                  
print("\n")
