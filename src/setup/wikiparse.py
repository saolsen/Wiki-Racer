#!/usr/bin/env python
# This is the script used to parse the wikipedia xml db dump into
# a redis database.

import sys
import re
from BeautifulSoup import BeautifulStoneSoup

__author__ = 'Stephen Olsen'

wikilink = re.compile(r'(\[\[)([-_a-zA-Z0-90-9.()|  ]*?)(\]\])')

def parsePage(page):
    """
    Takes a Wikipedia page string
    from the xml document <page>...</page>
    Returns a string representation of a graph node
    'pagename:link1,link2,link3' 
    """
   
    soup = BeautifulStoneSoup(page)
    node = soup.title.contents[0] + '|'

    for link in wikilink.findall(soup.text):
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
    soup = BeautifulStoneSoup(redirect)
    node = soup.title.contents[0] + '|'

    node += wikilink.search(soup.text).group(2)

    return node
 
def checkType(page):
    """
    Returns true if the page is a real wikipedia page and false if it is
    a redirect.
    """
    return not bool(re.search('<redirect />', page))

def main():
    """
    Takes a xml document and return two files, nodes and redirects
    """
    try:
        infile = sys.argv[1]
        f = open(infile, 'r')
        n = open('./nodes', 'a')
        r = open('./redirects' , 'a')

        page = []

        while True:
            line = f.readline()
            if not line:
                break
            if line.strip() == '<page>':
                while line.strip() != '</page>':
                    page.append(line)
                    line = f.readline()
                page.append(line)
                page_str = "".join(page)
                try:
                    if checkType(page_str):
                        node = parsePage(page_str)
                        n.write(node + '\n')
                        print 'Node: ', node
                    else:
                        redirect = parseRedirect(page_str)
                        r.write(redirect + '\n')
                        print 'Redirect: ', redirect
                except:
                    pass
                page = []
        f.close()
        n.close()
        r.close()
    except IndexError:
        print "Please specify an input file"

def mainPiCloud(filename, num):
    """
    Like the above but meant to be run on picloud. Takes a key for a
    file stored on piclouds datastore, runs the same analysis on it
    and returns a tuple of two new files stored on datastore
    (nodefile,redirectfile)
    """
    import cloud
    cloud.setkey(api_key='XXXX', \
    api_secretkey='XXXX')

    try:
        cloud.files.get(filename, './xml-parse')
        f = open('./xml-parse', 'r')
        n = open('./nodes', 'a')
        r = open('./redirects', 'a')

        page = []

        while True:
            line = f.readline()
            if not line:
                break
            if line.strip() == '<page>':
                while line.strip() != '</page>':
                    page.append(line)
                    line = f.readline()
                page.append(line)
                page_str = "".join(page)
                try:
                    if checkType(page_str):
                        node = parsePage(page_str)
                        n.write(node + '\n')
                    else:
                        redirect = parseRedirect(page_str)
                        r.write(redirect + '\n')
                except:
                    pass
                page = []
        f.close()
        n.close()
        r.close()
        cloud.files.put('./nodes', 'n' + str(num))
        cloud.files.put('./redirects', 'r' + str(num))
        return ('n' + str(num),r + str(num))
    except:
        return False

if __name__=="__main__":
    main()
