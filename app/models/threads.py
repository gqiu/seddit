import web
import string
import config
from app.models import people

#   module: threads

def getmessages(id):
    return web.select('messages', where='thread_id=%s' % web.sqlquote(id), _test=False)
    
def new(roomid, authorid, summary, question):
    id = web.insert('threads', room_id=roomid, summary=summary, question=question)
    newmessage(id, authorid, question)
    return id

def newmessage(thread, authorid, message):
    web.insert('messages', author_id=authorid, content=message, thread_id=thread)
    
def messageoffset(id, offset):
    messages = web.select('messages', where='thread_id = %s and id > %s' % (web.sqlquote(id), web.sqlquote(offset)))
    
    offsetmessages = []
    
    for message in messages:
        message['date_sent'] = web.datestr(message['date_sent'])
        message['author'] = people.getperson(message.author_id).name
        offsetmessages.append(message)
        
    return offsetmessages
    
def getthread(id):
    thread = web.select('threads', where='id=%s' % web.sqlquote(id), limit=1)
    
    if thread:
        return thread[0]
    else:
        return None
        
def threadtranscript(threadid):
    thread = getthread(threadid)
    messages = getmessages(threadid)
    lastmessage = 0 # see javascript api for more information
    
    thread = web.storify(thread)
    thread.date_started = web.datestr(thread.date_started)
    
    transcript = { 'thread': thread, 'messages': None }
    transcript = web.storify(transcript)
    
    transcript.messages = []
    
    for message in messages:
        transcript.messages.append({ 'id': message.id, 'author_id': message.author_id, 'author': people.getperson(message.author_id).name, 'content': message.content, 'time': web.datestr(message.date_sent)})
        lastmessage = message.id
        
    transcript.thread.last_message = lastmessage
    
    return transcript
    
def recent(roomid=None):
    if roomid:
        return web.select('threads', where='room_id=%i' % roomid, limit=5)
    else:
        return web.select('threads', limit=5)
        
#
#   refactored stuff
#

def find(id):
    # TODO getthread has the same functionality. replace this with getthread.
    thread = web.select('threads', where='id=%s' % web.sqlquote(id), limit=1)
    
    if thread:
        return thread[0]
    else:
        return None

class thread:
    def __init__(self, id):
        """docstring for __init__"""
        thread = web.select('threads', where='id=%s' % web.sqlquote(id), limit=1)
        if thread: self.thread = thread[0]
        else: raise ValueError, "can't find the entry for the given id"
    
    def __getitem__(self, key):
        return self.thread[key]
        
    def __setitem__(self, key, value):
        web.query('update threads set %s = %s where id = %s' % (key, web.sqlquote(value), self.thread['id']))
        
    def archive(self):
        """docstring for archive"""
        if self['resolved'] == 'True': return
        
        messages = self.getmessages()
        s = "<div id=\"chat_archive\">"
        t = string.Template('<div id="message_$id" class="line"><span class="author">$author</span><span id="message">$message</span></div>')
        
        for m in messages:
            s += t.substitute({'id': m.id, 'author': self._getauthor(m.author_id).name, 'message': m.content})
        s += "</div>"
        
        aid = web.insert('thread_archives', thread_id=self['id'], content=s)
        self['resolved'] = 'True'
        
        return aid
        
    def retrievearchive(self):
        """docstring for retrievearhive"""
        archive = web.select('thread_archives', where='thread_id=%s' % web.sqlquote(self['id']), limit=1)
        if not archive: archive = 'this thread hasn\'t been archived yet'
    
        return archive[0]
        
    def comments(self):
        """docstring for comments"""
        return web.select('archive_comments', where='thread_id=%s' % web.sqlquote(self['id']), order='id asc')

        
    def getmessages(self):
        """docstring for getmessages"""
        messages = web.select('messages', where='thread_id=%s' % web.sqlquote(self['id']))
        return messages
        
    def _getauthor(self, authorid):
        """docstring for _getauthor"""
        a = web.select('people', where='id=%s' % web.sqlquote(authorid), limit=1)
        if a: return a[0]
        else: return 'anonymous'
        
        
