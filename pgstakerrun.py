#! /usr/bin/python3
# coding: utf-8
# version 0.2

# from re import RegexFlag
import os, zipfile, re, sys
from os.path import exists
from bs4 import BeautifulSoup
from pgstakerfunc import getFolder as gf
from pgstakerfunc import extract as extr
from pgstakerfunc import pgstakelist
from pgstakerfunc import pgstakeregex
from pgstakerfunc import sortby
from findlistofclasses import findlistofclassesx

# ### get file name and validate
# import sys
# try:
#     inputFile = sys.argv[1] 
# except IndexError:
#     print("No file dropped")

### Set  directory of file
currDir = os.path.dirname(__file__)
os.chdir(currDir)
print(currDir)

#TEMP INPUT
inputFile=input("Please add file name (from test folder): ")

if not inputFile:
    inputFile = "test.epub"

### Check to see if the file exists
file_exists = os.path.exists(currDir + "/working/" + inputFile)
if not file_exists:
    print(inputFile + ' does not exist or is not in the test folder.')
    exit()

### Check to see if the ending is valid
if not inputFile.endswith(".epub"):
    print(inputFile + ' invalid name. File must be an epub')
    exit()

os.chdir("working") # change to working folder

### Use function to extract folder name
Exportfolder=gf(inputFile)
# print(Exportfolder)



### function to extract zipped files
extr(inputFile)

### set parameters, open file and write opening
pagestakerfilename=Exportfolder
pagestakerfile = open(pagestakerfilename +"-pagestaker.txt", "w")
pagestakerfile.write('<nav epub:type="page-list" role="doc-pagelist">\n\t<ol>\n')


### Get working folder and change directory
# print (Exportfolder)
os.chdir(Exportfolder)
print(os.getcwd())


### make some lists
items = []
filepagelist = []
completelist = []

### travese files and make a list of paths & files ending in xhtml
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".xhtml"):
            items.append(root + "/" + file)
# print(items)

### Loop through list
for file in items:
    # print(file)

    ### loop though file and extract html as soup
    with open(file, 'r') as inp:
        data = inp.read()
        soup = BeautifulSoup(data, "html.parser")

        ### Write pagestaker list function
        pgstakelist(file,soup,completelist)
 
        # RUN GET UNIQUELIST function
        uniquelist = findlistofclassesx(soup)

        ### run regex function
        data = pgstakeregex(data)
    # print(data)
    with open(file, 'w') as output:
        output.write(data)
        output.close()
# print(completelist)

### Sort returned list
completelist.sort(key=sortby)

### for each item write to the file
for inner_list in completelist:
    # print(inner_list[0])
    pagelist_item='\t\t<li><a href="' + inner_list[1] + '#page' +  str(inner_list[0]) + '">' + str(inner_list[0]) + '</a></li>\n'
    pagestakerfile.write(pagelist_item)

### write end of file and close
pagestakerfile.write('\n\t</ol>\n</nav>\n')

# TEMP WRITE OUTPUT TO FILE
pagestakerfile.write('\nLIST OF TAGS & CLASSES\n')
for tag in uniquelist:
    pagestakerfile.write("\t" + tag[0] + " " + tag[1] + "\n")

pagestakerfile.close()

# print(os.getcwd())

### Change back to top directory
os.chdir("..")

### Recompress files
if (os.path.isdir(Exportfolder)):
    epubFile = zipfile.ZipFile(Exportfolder + "_rev.epub", 'w', zipfile.ZIP_DEFLATED)
    
    os.chdir(Exportfolder)
    
    for root, dirs, files in os.walk("."):
        for file in files:
            # print(root, file)
            epubFile.write(os.path.join(root, file))
    epubFile.close()
else:
    print("wrong directory")


### Change back to top directory
os.chdir("..")
# print(os.getcwd())
