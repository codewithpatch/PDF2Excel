from tika import parser
import pprint
from collections import defaultdict
import re
import pandas as pd

pp = pprint.PrettyPrinter(indent=4)

parsedPDF = parser.from_file("samplePDF.pdf")
#pp.pprint(parsedPDF)

# Get the content of the PDF file and convert it into a LIST
content = parsedPDF['content']
contentlist = content.split('\n')

# Remove empty strings in the list resulting from the split
contentlist = list(filter(lambda a: a != '', contentlist))

# pp.pprint(contentlist)


# Create an iterator and other flags that I will use to for the algorithm
iterateContent = iter(contentlist)      # Iterator of the contents of PDF per line
data = defaultdict(dict)                # Dictionary placeholder of the data scraped
cntr = 0                                # Our counter to count how many blocks did we able to get
line = 1                                # Indicator which line are we in a specific block of data

while True:
    # The algorithm will use the flags cntr and line to determine if we are in a new block or existing block
    try:
        string = next(iterateContent)
    except StopIteration:
        break

    # Once we matched a name, this means that we are in a new block.
    # The if-elif blocks below saves the variable into a dictionary that will be later be use as the data that
    #       we will export into excel
    if re.match('^[A-Z\s]+$', string):
        cntr += 1           # We increment cntr to determine that we are in a new block

        data[cntr]['name'] = string
        line = 2            # Line is set to two to indicate that the next loop is line 2 of current block
        print('matched')

    elif line == 2:
        data[cntr]['Street Address'] = string
        line += 1

    elif line == 3:
        data[cntr]['State'] = string
        line += 1

    elif line == 4:
        data[cntr]['ContactNumber'] = string
        line += 1

    elif line == 5:
        data[cntr]['Other Contact# 1'] = string
        line += 1

    elif line == 6:
        data[cntr]['Other Contact# 2'] = string
        line += 1

    # End of Block

print("Total data:", len(data.keys()))
#pp.pprint(data.values())

# Setting up the data into Dataframe
df = pd.DataFrame(data.values())
df.index += 1
print(df)

# Write the dataframe into excel
writer = pd.ExcelWriter("dataframe.xlsx", engine='xlsxwriter')
df.to_excel(writer, sheet_name='output', index=False)
writer.save()
