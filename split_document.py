#!/usr/bin/env python3
""" SplitDocument.py
Separate a single text document into multple documents based on a 
collection of possible delimeters. In this case the source document
is delimited by date. The date can be in several formats. For each
document section, create a new file named with the date in the delimeter.
For each section, the date is converted to a standard form to be used as the
file name.
"""
import datetime
import sys
from dateutil.parser import parse

def check_date(line):
    """Check if the line is a date"""
    try:
        date = parse(line[0:25], fuzzy_with_tokens=True)
        # Make sure the date is before today
        if date[0].date() >= datetime.datetime.today().date():
            return None
        # Find the index of the remaining text after the date. There should be no text before the date
        if date[1][0].strip().isalpha():
            return None
        # Is there any text after the date?
        if date[1][-1].strip() == '':
            index = -1
        else:
            index = line.find(date[1][-1]) + 1
        return (date[0], index)
    except ValueError:
        return None

def main(source):
    delimeter = True
    outfile = None
    for line in source:
        # Did we get a blank line? If so, read the next line
        if len(line.strip()) == 0:
            delimeter = True
            continue
        # If the previous line was a delimeter, check if a new file or new paragraph
        if delimeter:
            date = check_date(line)
            if date is None:
                # We have a paragraph
                outfile.write('\n')
                outfile.write(line)
            else:
                if outfile is not None:
                    outfile.close()
                # Create a new file   
                outfile = open(date[0].strftime('%Y-%m-%d') + '.md', 'w')       
                # Write the date line
                outfile.write(date[0].strftime('***%A, %I:%M %p***') + '\n')
                # Find the first words in the line
                if date[1] > 0:
                    text = line[date[1]:]
                    outfile.write(text)
            delimeter = False
            continue
        # If the previous line was not a delimeter, write the text
        outfile.write(line)
    if outfile is not None:
        outfile.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please provide the file you want to split")
        exit(1)
    else:
        raw_file = sys.argv[1]
    try:
        with open(raw_file, 'r') as file:
            main(file)
    except FileNotFoundError:
        print("File not found")
