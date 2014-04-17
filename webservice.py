#! /usr/bin/python
"""
base cherrypy launcher for the IPOL webservice app
"""

import cherrypy
import sqlite3
import os
import json


class DemoStats(object):
    """ Defines pages associated to demo archive statistics """

    @cherrypy.expose
    def stat(self, **kwargs):
        """
        Page of demo stat
        """
        if 'demo' in kwargs:
            demo_id = kwargs['demo']
            stat = self.get_demo_stats(demo_id)
            if stat:
                return json.dumps(stat)
            else:
                return "unknow demo key: %s " % demo_id
        else:
            return "no demo ID given"


    def get_demo_stats(self, demo_id):
        """
        Get stats from id and database
        """
        demodb = os.path.abspath(os.path.join(base_dir, \
                                 "app/%s/archive/index.db" %demo_id))
        print demodb
        try:
            database = sqlite3.connect(demodb)
            curs = database.cursor()
            curs.execute("select count(*) from buckets where public=1")
            public = curs.next()[0]
            curs.execute("select count(*) from buckets where public=0")
            private = curs.next()[0]
            return {"public": public, "private": private,
                    "total": public + private}
        except (IOError, sqlite3.Error):
            return None

if __name__ == '__main__':

    # location settings
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print base_dir
    cherrypy.quickstart(DemoStats())
