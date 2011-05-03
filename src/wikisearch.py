#!/usr/bin/env python
"""
Finds the shortest path between two wikipedia nodes
AI final project
"""

import json
import httplib2
import urllib
import sys
import re
from collections import deque

__author__ = 'Stephen Olsen'

class WikiSearcher:
    def __init__(self, start_title, goal_title):
        self.conn = httplib2.Http()
        self.start_node = self._getPage(start_title)
        self.goal_node = self._getPage(goal_title)
        if self.start_node and self.goal_node:
            self.node_paths = {self.start_node.title: [self.start_node.title]}
            self.queue = deque([self.start_node.title])
        else:
            raise Exception('Invalid Pages')

    def Search(self):
        # BFS to find the shortest path to the goal node.
        while True:
            try:
                label = self.queue.popleft()
                node = self._getPage(label)
                if node:
                    if self.goal_node.title in node.links:
                        return self.node_paths[label] + [self.goal_node.title]
                        break
                    # Make sure we didn't miss it on the last pass due to wikipedia sending
                    # bad title names (it happens)
                    elif node.title == self.goal_node.title:
                        return self.node_paths[label]
                    else:
                        for child in node.links:
                            fake_link = bool(re.match("Category", child) or re.match("Template", child)
                                        or re.match("Portal", child) or re.match("Wikipedia", child)
                                        or re.match("Help", child) or re.match("File", child))
                            if child not in self.node_paths and not fake_link:
                                self.queue.append(child)
                                self.node_paths[child] = self.node_paths[label] + [child]
                                print child
            except Exception as e:
                print sys.exc_info()[0]
                print e
                return "Path doesn't seem to exist."
    
    def _getPage(self, title):
        more_links = True
        links = []
        params = {'action': 'query', 'prop': 'links', 'pllimit': '500', 'format': 'json'}
        params['titles'] = title

        try:
            while more_links:
                resp, content = self.conn.request("http://en.wikipedia.org/w/api.php?redirects&"
                                                  + urllib.urlencode(params))
                page = json.loads(content)
                pageid = page['query']['pages'].keys()[0]
                if pageid != '-1':
                    for link in page['query']['pages'][pageid]['links']:
                        links.append(link['title'])
                        if 'query-continue' in page:
                            params['plcontinue'] = page['query-continue']['links']['plcontinue']
                        else:
                            more_links = False
                else:
                    more_links = False
                    links = [];
            if links != []:
                return Node(page['query']['pages'][pageid]['title'], links)
            else:
                return False
        except:
            print "Might want to check your internet connection"
            return False

class Node:
    def __init__(self, title, links):
        self.title = title;
        self.links = links; #Should be a list

def main(start_title, goal_title):
    try:
        search = WikiSearcher(start_title, goal_title)
        return search.Search()
    except Exception as e:
        return str(e)

if __name__=="__main__":
    s = raw_input("Enter state page: ")
    g = raw_input("Enter goal page: ")
    print main(s, g)
