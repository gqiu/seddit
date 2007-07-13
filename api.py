import view
import db
import simplejson
from view import render


class sendmessage:
    def POST(self):
        """ Do add a new message into the database, given a thread id
        
            the message expects the following parameters
                - thread_id
                - author
                - message
        """
        i = web.input()
        db.sendmessage(threadid, author, message)
        
class poll:
    def GET(self, threadid):
        dataset = db.getlog(threadid)
        mlist = []
        
        for m in dataset:
            mlist.append({ 'id': m.id, 'user': m.author, 'text': m.content, 'time': '%s' % m.date_sent } )
            
        messages = { 'messages': { 'message': mlist } }
        print simplejson.dumps(messages)
        