import csv

valid_cards = "123456789XJQK"

result = []

with open('data2.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        # each letter is represented by a char
        # spaces are spaces
        value = row[0]
        suit = row[1]

        value = value.replace(' ', '')
        suit = suit.replace(' ', '')

        if len(value) != len(suit):
            print("SUIT AND STRING LEN MISMATCH! on row:\n{}".format(row))
            print("value len: {}; suit len: {}".format(len(value), len(suit)))

        outRow = ""

        for i in range(len(value)):
            if i < len(value) and i < len(suit):
                val = value[i]
                suit2 = suit[i]
                if val != ' ' and suit2 != ' ' and val in valid_cards:

                    if suit2 == 'S':
                        outRow += val

                    else:
                        isClubs = suit2 == 'C'

                        # offset NOT clubs by 13
                        offset = 13 if not isClubs else 0

                        # handle facecards
                        if val == 'X':
                            val = 10
                        if val == 'J':
                            val = 11
                        if val == 'Q':
                            val = 12
                        if val == 'K':
                            val = 13

                        offsetVal = chr(ord('A') - 1 + int(val) + offset)
                        outRow += offsetVal
                else:
                    outRow += value[i]
                
        result.append(outRow)
                
print()
for row in result:
    print(row)
print()