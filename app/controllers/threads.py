import web
import config
import simplejson

from web import form

from app.models import threads
from app.models import rooms

from app.utilities import auth

view = web.template.render('app/views/threads/', cache=config.cache)
person = auth.getuser()

qform = form.Form(
    # TODO use the full name of the room, and use the id name as the unique identifier.
    form.Dropdown('rooms', [(r.id, r.title) for r in rooms.getrooms()]),
    form.Textbox('summary', form.notnull),
    form.Textarea('question'),
)

class transcript:
    def GET(self, id):
        # TODO if a trasncript is requested for an invalid thread id, tell the user.
        print simplejson.dumps(threads.threadtranscript(id))
        
class chat:
    def GET(self, id):
        transcript = threads.threadtranscript(id)
        print config.base.thread(view.thread(transcript.thread, transcript.messages, auth.getuser()), 'thread')
        
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

class ask:
    def GET(self): 
        form = qform()
        print config.base.layout(view.ask(form), person)

    def POST(self): 
        form = qform() 
        if not form.validates(): 
            print config.base.layout(view.ask(form), person)
        else:
            id = threads.new(question=form.d.question, roomid=form.d.rooms, summary=form.d.summary)
            web.seeother('/thread/%i' % id)