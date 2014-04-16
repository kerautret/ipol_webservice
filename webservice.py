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
            if stat is not None:
                return  stat
            else:
                return "unknow demo key: %s " % demo_id
        else:
            return "No demo ID given. "
    stat.exposed = True



    def get_demo_stats(self, demo_id):
        """
        Get stats from id and data base
        """
        demodb = os.path.abspath(os.path.join(base_dir, \
                                  "../demo/app/%s/archive/index.db" %demo_id))
        if os.path.isfile(demodb):
            database = sqlite3.connect(demodb)
            curs = database.cursor()
            curs.execute("select count(*) from buckets where public=1")
            result = curs.next()
            return json.dumps({"total exeperiments": result[0]})
        else:
            return None



if __name__ == '__main__':

    # config file and location settings
    base_dir = os.path.dirname(os.path.abspath(__file__))
    demo_dir = os.path.abspath(os.path.join(base_dir, '../demo/'))
    app_dir = os.path.abspath(os.path.join(base_dir, '../demo/app'))

    cherrypy.quickstart(DemoStats())
