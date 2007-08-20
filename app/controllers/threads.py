import web
import config
import simplejson

from web import form

from app.models import threads
from app.models import rooms

from app.utilities import auth

view = web.template.render('app/views/threads/', cache=config.cache)
person = auth.getuser()

def getquestion():
    input = web.input()
    try:
        if input.question:
            return input.question
        else:
            return ''
    except AttributeError:
        pass
        
qform = form.Form(
    form.Dropdown('rooms', [(r.id, r.title) for r in rooms.getrooms()]),
    form.Textbox('summary', form.notnull),
    form.Textarea('question', value=getquestion()),
)

commentform = form.Form(
    form.Textarea('comment', form.notnull),
    form.Hidden('author_id', value=person.id)
)

class transcript:
    def GET(self, id):
        # TODO if a trasncript is requested for an invalid thread id, tell the user.
        print simplejson.dumps(threads.threadtranscript(id))
        
class chat:
    def GET(self, id):
        transcript = threads.threadtranscript(id)
        threads.updaterecent(person.id, id)
        recent = threads.getrecent(person.id, limit=2)
        print config.base.thread(view.thread(transcript.thread, transcript.messages, auth.getuser()), recent, 'thread')
        
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
        i = web.input()
        q = ''
        try:
            if i.question:
                form.d.question = i.question
        except AttributeError:
            pass
            
        print config.base.layout(view.ask(form, q), person)

    def POST(self):
        form = qform()
        if not form.validates(): 
            print config.base.layout(view.ask(form), person)
        else:
            id = threads.new(question=form.d.question, authorid=person.id, roomid=form.d.rooms, summary=form.d.summary)
            web.seeother('/thread/%i' % id)
            
class search:
    def GET(self):
        input = web.input()
        query = None
        results = None
        try:            
            if input.q:
                query = input.q
        except AttributeError:
            pass
        
        if query:
            results = threads.search(query)
        
        print config.base.layout(view.search(query, results), person)
            
class resolve:    
    def GET(self, id):
        """ marks the thread as resolved
        
            NOTE only the user that asked the question, can mark the question as resolved. In the future
            i think that admins will be able to close questions as well, but for now, i haven't
            implemented that yet.
            
            TODO check to make sure the user trying to close the thread is the originating user.
        """
        thread = threads.thread(id)
        aid = thread.archive()
        web.seeother('/thread/%i/archive/' % thread['id'])
        
class archive:
    def GET(self, id):
        """ displays the requested thread as an archived webpage.
        """
        thread = threads.thread(id)
        comments = thread.comments()
        f = commentform()
        print config.base.layout(view.archive(thread.retrievearchive(), comments, f), person)
        
    def POST(self, id):
        """ applies any changes made to the archived page.
        
            TODO provide a reset button, so if someone screws up the page, they can still fix it.
        """
        pass
        
class comment:
    def POST(self, id):
        f = commentform()
        
        if not f.validates():
            web.seeother('/thread/%s/archive/' % id)
        else:
            cid = web.insert('archive_comments', thread_id=id, author_id=f.d.author_id, message=f.d.comment)
            web.seeother('/thread/%s/archive/' % id)
        
        
        
        