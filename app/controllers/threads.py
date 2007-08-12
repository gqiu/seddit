import web
import config
import simplejson

from app.models import threads

class transcript:
    def GET(self, id):
        # TODO if a trasncript is requested for an invalid thread id, tell the user.
        print simplejson.dumps(threads.threadtranscript(id))
        
class poll:
    def GET(self, id, offset):
        messages = threads.messageoffset(id, offset)
        print simplejson.dumps(messages)
        
class say:
    def POST(self, threadid):
        input = web.input()
        threads.newmessage(threadid, input.author, input.message)
        
class new:
    def POST(self):
        input = web.input()
        threads.new(roomid = input.roomid, question = input.question)
        