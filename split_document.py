#!/usr/bin/env python3
""" SplitDocument.py
Separate a single text document into multple documents based on a 
collection of possible delimeters. In this case the source document
is delimited by date. The date can be in several formats. For each
document section, create a new file named with the date in the delimeter.
For each section, the date is converted to a standard form to be used as the
file name.
"""
import sys
from dateutil.parser import parse

def check_date(line):
    """Check if the line is a date"""
    try:
        date = parse(line)
        return date
    except ValueError:
        return None

def remove_date(line):
    """Remove the date from the line. We assume the date is at the beginning of the line"""
    words = line[15:-1].split(' ')
    text = ' '.join([alpha for alpha in words if alpha.isalpha()])

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
                text = '\n'
            else:
                if outfile is not None:
                    outfile.close()
                # Create a new file   
                outfile.open(date.strftime('%Y-%m-%d') + '.md', 'w')       
                # Write the date line
                outfile.write(date.strftime('%d/%m/%Y, %H:%M:%S') + '\n')
                # Find the first words in the line
                text = remove_date(line)
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
