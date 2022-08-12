#! /usr/local/bin/python3
# coding: utf-8

### Search for page-stakes and make list
### version.001

# from dataclasses import replace
# import glob, 
import os, zipfile, re
# from posixpath import curdir
from bs4 import BeautifulSoup

### Set input (TEMP) and change directory
# print('Enter epub file name (default is test.epub):')
# filename = input()


import sys
try:
    inputFile = sys.argv[1] 
except IndexError:
    print("No file dropped")

# if filename == "":
#     inputFile = "test.epub"
# else:
#     inputFile = filename

### Check to see if the ending is valid
if not inputFile.endswith(".epub"):
    print(inputFile + ' invalid name. File must be an epub')
    exit()

currDir = os.path.dirname(__file__)
os.chdir(currDir)

### split out folder name from file name
Exportfolder =  os.path.splitext(inputFile)[0]
pagestakerfilename=Exportfolder

### Define search and replace regexs
search_text = r'<span class="com-rorohiko-pagestaker-style.*?">(\d+?|(x{0,3})(ix|iv|v?i{0,3})?)</span>'
replace_text = lambda x:'<span epub:type="pagebreak" role="doc-pagebreak" id="page' + x.group(1) + '" title="' + x.group(1) + '" />'

### Extract files
epubFile = zipfile.ZipFile(inputFile, 'r')
epubFile.extractall(inputFile[:-5])
epubFile.close()


### open file
# pagestakerfile = open(currDir+"/" +pagestakerfilename +"-pagestaker.txt", "w")
pagestakerfile = open("/" +pagestakerfilename +"-pagestaker.txt", "w")

### Write opening to file
pagestakerfile.write('<nav epub:type="page-list" role="doc-pagelist">\n\t<ol>\n')

### Get working folder and change directory
# print (Exportfolder)
os.chdir(Exportfolder)


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

    with open(file, 'r') as inp:
        data = inp.read()
        ### Write pagestaker list
        soup = BeautifulSoup(data, "html.parser")
        # pagelist = soup.find_all('span',{'class':'com-rorohiko-pagestaker-style'})
        for pagelist in soup.select('span.com-rorohiko-pagestaker-style'):
            # print(file, pagelist)
            ### remove OEBS folder from filepath
            filepath = re.sub(r'\./OEBPS/', '', file, count = 1)
            page = pagelist.contents[0].strip()
        #     page = i.contents[0]
            if page.isdigit():
                page=int(page)

            filepagelist=(page,filepath)
            completelist.append(filepagelist)

        ### Replace pagestaker spans
        data = re.sub(search_text, replace_text, data)
        # print(data)
    
    with open(file, 'w') as output:
        output.write(data)
        output.close()

### a function to grab page, turn it into an interger (unless it is a roman numeral), and then designate it as a sort key
def sortby(x):
    try:
        return int(x[0])
    except ValueError:
        return float('inf')

completelist.sort(key=sortby)
# print(completelist)

### for each item write to the file
for inner_list in completelist:
    print(inner_list[0])
    pagelist_item='\t\t<li><a href="' + inner_list[1] + '#page' +  str(inner_list[0]) + '">' + str(inner_list[0]) + '</a></li>\n'

    pagestakerfile.write(pagelist_item)

#write end of file and close
pagestakerfile.write('\n\t</ol>\n</nav>')
pagestakerfile.close()

os.chdir("..")
print(os.getcwd())   

### Recompress files
print 
if (os.path.isdir(Exportfolder)):
    epubFile = zipfile.ZipFile(Exportfolder + "_rev.epub", 'w', zipfile.ZIP_DEFLATED)
    
    os.chdir(Exportfolder)
    
    for root, dirs, files in os.walk("."):
        for file in files:
            print(root, file)
            epubFile.write(os.path.join(root, file))
    epubFile.close()
    
### Change back to top directory
os.chdir("..")
