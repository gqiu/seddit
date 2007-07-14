import view
import web
import db
import simplejson
from view import render


class post:
    def POST(self):
        """ Do add a new message into the database, given a thread id
        
            the message expects the following parameters
                - threadid
                - author
                - message
        """
        i = web.input()
        db.sendmessage(i.threadid, i.author, i.message)
        
class getlog:
    def GET(self, threadid):
        dataset = db.getlog(threadid)
        print jsonformessage(dataset)
        
class getthreadupdates:
    def GET(self, threadid, lastid):
        dataset = db.getthreadupdates(threadid, lastid)
        print jsonformessage(dataset)
        
        
#
#   Utility Methods
#
def jsonformessage(dataset):
    """Return JSON formatted string given a sql dataset for messages"""
    mlist = []

    for m in dataset:
        mlist.append({ 'id': m.id, 'user': m.author, 'text': m.content, 'time': '%s' % m.date_sent } )
        
    messages = { 'messages': { 'message': mlist } }
    return simplejson.dumps(messages)