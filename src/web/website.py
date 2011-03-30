#!/usr/bin/env python
import sys
sys.path.append("../")

import web
#import search.whatever it's called

urls = (
    '/', 'index')

app = web.application(urls, globals())

class index:
    def GET(self):
        return "Wikipedia Racer, the shortest path between two pages."

if __name__ == "__main__":
    app.run()
