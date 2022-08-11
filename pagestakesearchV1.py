### Search for page-stakes and make list

from dataclasses import replace
import glob, os, zipfile, re
from posixpath import curdir
from bs4 import BeautifulSoup

### Set input (TEMP) and change directory
currDir = os.path.dirname(__file__)
os.chdir(currDir)
inputFile ="test.epub"

Exportfolder =  os.path.splitext(inputFile)[0]
pagestakerfilename=Exportfolder

### Define search and replace regexs
search_text = r'<span class="com-rorohiko-pagestaker-style.*?">(\d+?)</span>'
replace_text = lambda x:'<span epub:type="pagebreak" role="doc-pagebreak" id="page' + x.group(1) + '" title="' + x.group(1) + '" />'


### Extract files
epubFile = zipfile.ZipFile(inputFile, 'r')
epubFile.extractall(inputFile[:-5])
epubFile.close()

### Get working folder and change directory
# print (Exportfolder)
if (os.path.isdir(Exportfolder)):
    os.chdir(Exportfolder)

### open file
pagestakerfile = open(currDir+"/" +pagestakerfilename +"-pagestaker.txt", "w")

### Write opening to file
pagestakerfile.write('<nav epub:type="page-list" role="doc-pagelist">\n\t<ol>\n')

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

