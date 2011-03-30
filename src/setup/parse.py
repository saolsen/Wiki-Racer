#!/usr/bin/env python
"""
    This is the script used to parse the wikipedia xml db dump into
    a redis database.
"""

__author__ = 'Stephen Olsen'

def parsePage(page):
"""
    Takes a Wikipedia page from the xml document <page>...</page>
    Returns a string representation of a graph node
    'pagename:link1,link2,link3' 
"""
    return 'fakepage:alpha,beta,gamma'

def parseRedirect(redirect):
"""
    Takes a Wikipedia redirect page from the xml document
    Returns a string representation of a redirect
    'pagename:real_link'
"""
    return 'fakelink:reallink'
 
def checkType(page):
"""
    Returns true if the page is a real wikipedia page and false if it is
    a redirect.
"""
    return true

def main(document_name):
"""
    Take a xml document and return two files, nodes and redirects
"""

    #Go through the file page by page,
    #use a simple regex to get everything between the two <data> or whatever
    #pages.

    #Parse that string. This way I dont need a real xml parser and I get to
    #learn regex and I get to iterate through the file instead of trying
    #to read in the whole thing at once.


    pass

if __name__=="__main__":
    main()
