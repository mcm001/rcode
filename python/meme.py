# User_00001_EMAIL=[cs7043@att.com]
# User_00001_FULLNAME=[Corey Swift]
# User_00001_PW=[emATchEC]
# User_00001_ADMIN=0
# User_00002_EMAIL=[as643e@att.com]
# User_00002_FULLNAME=[Ali  Senkayi]
# User_00002_PW=[9jtKwTQS]
# User_00002_ADMIN=0

import csv

fileData = open("C:\\Users\\robotics\\Downloads\\licensecsv.csv").read()
# newStr = [ '"{}"'.format(x) for x in list(csv.reader([fileData], delimiter=',', quotechar='"'))[0] ]

with open("C:\\Users\\robotics\\Downloads\\licensecsv.csv", 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

print(reader)