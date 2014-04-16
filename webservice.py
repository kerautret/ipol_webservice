#! /usr/bin/python
"""
base cherrypy launcher for the IPOL webservice app
"""

import cherrypy
from mako.lookup import TemplateLookup
import sqlite3
import os
import shutil
import json


class DemoStats(object):
 
 @cherrypy.expose
 def stat(self,  **kwargs):
     if 'demo' in kwargs:
         demoID = kwargs['demo']
         stat = self.getDemoStats(demoID)
         if stat is not None :
             return  stat 
         else:
             return "unknow demo key: %s " % demoID
     else:
         return "No demo ID given. "
 stat.exposed = True



 def getDemoStats(self, demoID):
     demodb = os.path.abspath(os.path.join(base_dir, "../demo/app/%s/archive/index.db" %demoID ))
     if os.path.isfile(demodb) :
         db = sqlite3.connect(demodb)
         c = db.cursor()
         c.execute("select count(*) from buckets where public=1")     
         result = c.next()
         return json.dumps({"total exeperiments": result[0] })
     else:
        return None

    

if __name__ == '__main__':

    import sys
    # config file and location settings
    base_dir = os.path.dirname(os.path.abspath(__file__))
    demo_dir = os.path.abspath(os.path.join(base_dir, '../demo/'))
    app_dir = os.path.abspath(os.path.join(base_dir, '../demo/app'))
    print app_dir
    sys.path.append(demo_dir)

    from app import demo_dict
   
    for (demo_id, demo_app) in demo_dict.items():
        print demo_id

    cherrypy.quickstart(DemoStats())
        
