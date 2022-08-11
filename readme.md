# Background
When making accessible ebooks a page list is supposed to be included in the nav doc that matches the original print publication.

Currently the easiest way to do this is using the pagestaker script developed by rorohiko and Laura Brady. Unfortunately the acommpanying app 'epubgrify' (a php-based script) which finds the tags created by the pagestaker script and creates a list no longer works.

This python script is an attempt to fill that gap.

## Dependancies:
- python 3
- BeautifulSoup


# Method
The script: 
1. decompresses the file (**currently a test file called test.epub**) into a folder
2. opens a text file
1. walks through all the files and
    1. finds all files that end in .xhtml
    2. uses Beautiful Soup to find all spans with a class "com-rorohiko-pagestaker-style". will valiate for page numbers or lowercase roman numerals up to 39
    1. writes the page# and file name to list
    1. performs a reges search and replace to replace span with appropriate epub:type and role
    1. sorts the list by page# (**note** roman numerals are sorted to the end)
1. writes list to text file
1. compresses epub again with new name

  You will then need to open the epub and paste the contents of the file in the nav doc and ensure the sort order is correct.

# To use
You will need to have python 3 installed. Most Macs have python 2 installed out of the box so you will need to update. You will also need to install the BeautifulSoup package.

Put the epub file in the same location as the script. Open Terminal, type `cd ` and drag the folder into the window and hit enter to change the directory. Run the script by typing `python3 pagestakesearchV1.py` in terminal. 

# Note
There is a Sigil plugin here [https://www.mobileread.com/forums/showthread.php?t=265237] that basically does the same thing. You simply have to edit the preferences json file to look for `com-rorohiko-pagestaker-style`. But I will keep plugging away on my own version...