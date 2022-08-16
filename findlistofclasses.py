#! /usr/local/bin/python3
# coding: utf-8


from bs4 import BeautifulSoup
import re

# functon to find unique entries
def get_unique_numbers(listofclasses):
    unique = []

    for number in listofclasses:
        if number in unique:
            continue
        else:
            unique.append(number)
    return unique


def findlistofclassesx(soup):
    # soup = BeautifulSoup(text, "html.parser")

    #find all tags (elements)
    tags = {tag.name for tag in soup.find_all()}

    # create empty set becasue sets  don't have duplicates
    listofclasses = []

    #loop through tags (elements)
    for tag in tags:
        # find all element of tag
        for i in soup.find_all( tag ):  
            # if tag has attribute of class
            if i.has_attr( "class" ):
                # add tuple with tag and reatin space in classes
                found_class=i['class']
                for x in found_class:
                    listofclasses.append([tag,x])

    
    # print( listofclasses )
    uniquelistofclasses=(get_unique_numbers(listofclasses))
    return(uniquelistofclasses)

# sample html
sample = """
<body>
<div>
    <p id="alex">Alex</p>
    <p class="c1 c2">Alex</p>

    <p class="Bob">Bob</p>
    <p id="cathy">Cathy</p>
</div>
<ul class="abc">
    <li class="category">
        <i class="fa icon-cat"></i>
        <a href="#">Red</a>
    </li>
    <li class="category">
        <i class="fa icon-cat"></i>
        <a href="#">Black</a>
    </li>
    <li class="tree">
        <i class="fa-icon-cat"></i>
        <a href="#">Blue</a>
        <i class="tree"></i>
        <a href="#">Blue</a>
    </li>
</ul>
</body
"""