#!/usr/bin/env python
# This is the script used to parse the wikipedia xml db dump into
# a redis database.

import re
from BeautifulSoup import BeautifulStoneSoup

__author__ = 'Stephen Olsen'

def parsePage(page):
    """
    Takes a Wikipedia page string
    from the xml document <page>...</page>
    Returns a string representation of a graph node
    'pagename:link1,link2,link3' 
    """
    # page is a string of the page xml
    soup = BeautifulStoneSoup(page)
    node = soup.title.contents[0] + '|'

    for link in re.findall(r'(\[\[)([-_a-zA-Z0-90-9.()|  ]*?)(\]\])', soup.text):
        rename = link[1].find('|')
        if rename >= 0:
            node += link[1][rename+1:] + ','
        else:
            node += link[1] + ','
    node = node[:-1]

    return node

def parseRedirect(redirect):
    """
    Takes a Wikipedia redirect page from the xml document
    Returns a string representation of a redirect
    'pagename:real_link'
    """
    return 'AccessibleComputing:Computer accessibility'
 
def checkType(page):
    """
    Returns true if the page is a real wikipedia page and false if it is
    a redirect.
    """
    return true

def main(document_name):
    """
    Takes a xml document and return two files, nodes and redirects
    """

    #Go through the file page by page,
    #use a simple regex to get everything between the two <data> or whatever
    #pages.

    #Parse that string. This way I dont need a real xml parser and I get to
    #learn regex and I get to iterate through the file instead of trying
    #to read in the whole thing at once.

    # Get the file line by line, each time I have a page, join them and send
    # the string to the right fuction.

    pass

if __name__=="__main__":
    main()
