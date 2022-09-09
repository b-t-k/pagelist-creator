#! /usr/local/bin/python3
# coding: utf-8

#pgstakerfunc.py

import os, zipfile, re
from bs4 import BeautifulSoup

### split out folder name from file name and change directory
def getFolder(inputFile):
    Exportfolder =  os.path.splitext(inputFile)[0]

    return(Exportfolder)

### Define search and replace regexs
search_text = r'<span class="com-rorohiko-pagestaker-style.*?">(\d+?|(x{0,3})(ix|iv|v?i{0,3})?)</span>'
replace_text = lambda x:'<span epub:type="pagebreak" role="doc-pagebreak" id="page' + x.group(1) + '" title="' + x.group(1) + '" />'

### Extract files
def extract(inputFolder):

    epubFile = zipfile.ZipFile(inputFolder, 'r')
    epubFile.extractall(inputFolder[:-5])
    epubFile.close()

### replace pagestaker
def pgstakelist(file,soup, completelist):
    filepagelist = []
    for pagelist in soup.select('span.com-rorohiko-pagestaker-style'):
        # print(file, pagelist)

        ### remove OEBS folder from filepath
        filepath = re.sub(r'\./OEBPS/', '', file, count = 1)
        # print(pagelist.contents[0])
        if len(pagelist.contents[0]) != 0:
            page = pagelist.contents[0].strip()
            # print(page,filepath)
            if page.isdigit():
                page=int(page)

            filepagelist=(page,filepath)
            # print(filepagelist)
            ### Add page file list to complete list
            completelist.append(filepagelist)
    return(completelist)

### Replace pagestaker spans
def pgstakeregex(data):
    ### Define search and replace regexs
    search_text = r'<span class="com-rorohiko-pagestaker-style.*?">(\d+?|(x{0,3})(ix|iv|v?i{0,3})?)</span>'
    replace_text = lambda x:'<span epub:type="pagebreak" role="doc-pagebreak" id="page' + x.group(1) + '" title="' + x.group(1) + '" />'

    ### Run regex
    newdata = re.sub(search_text, replace_text, data)
    # print(newdata)
    return(newdata)
    
### a function to grab page, turn it into an interger (unless it is a roman numeral), and then designate it as a sort key
def sortby(x):
    try:
        return int(x[0])
    except ValueError:
        return float('inf')

