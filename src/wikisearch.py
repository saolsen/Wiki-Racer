#!/usr/bin/env python
# Finds the shortest path between two wikipedia nodes
# AI final project

import json
import httplib2
import urllib
import sys
from collections import deque

__author__ = 'Stephen Olsen'

class WikiSearcher:
    def __init__(self, start_title, goal_title):
        self.conn = httplib2.Http()
        self.start_node = self._getPage(start_title)
        self.goal_node = self._getPage(goal_title)
        # All the nodes returned so far with their path to the top.
        self.node_paths = {self.start_node.title: [self.start_node.title]}
        self.queue = deque([self.start_node.title])

    def Search(self):
        # BFS to find the shortest path to the goal node.
        while True:
            try:
                node = self._getPage(self.queue.popleft())
                if node:
                    if self.goal_node.title in node.links:
                        return self.node_paths[node.title] + [self.goal_node.title]
                    else:
                        for child in node.links:
                            print child
                            if child not in self.node_paths:
                                self.queue.append(child)
                                self.node_paths[child] = self.node_paths[node.title] + [child]
            except:
                print sys.exc_info()[0]
                return False
    
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
            return Node(page['query']['pages'][pageid]['title'], links)
        except:
            print "Might want to check your internet connection"
            return False

class Node:
    def __init__(self, title, links):
        self.title = title;
        self.links = links; #Should be a list

def main(start_title, goal_title):
    search = WikiSearcher(start_title, goal_title)
    return search.Search()
    

if __name__=="__main__":
    s = raw_input("Enter state page: ")
    g = raw_input("Enter goal page: ")
    print main(s,g)

