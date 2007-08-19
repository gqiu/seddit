import web
import string
import config
from app.models import people
from app.models import rooms

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
        
def updaterecent(userid, threadid):
    """ updates the user's 'recent_threads' column with the new thread that they just visited
    
        returns the updated thread list.
        
        TOOD refactor this, it's a prety ugly implementation of recent threads.
    """
    threadlist = people.getperson(userid).recent_threads
    recent = []
    
    if threadlist:
        recent = threadlist.split(' ')    
    if threadid in recent:
        recent.remove(threadid)
        
    recent.insert(0, threadid)
    
    print recent
    
    text = recent.pop(0) # take care of the fence post.
    for r in recent:
        text += ' ' + r

    web.update('people', where='id=%s' % web.sqlquote(userid), recent_threads=text)
    return 'threads'
    
def getrecent(userid, limit=5):
    recentthreads = people.getperson(userid).recent_threads
    tlist = recentthreads.split(' ')
    threads = []
    
    if len(tlist) > limit:
        tlist = tlist[0:limit]

    for t in tlist:
        thread = web.select('threads', where='id=%s' % web.sqlquote(t), limit=1)
        if thread:
            cur = thread[0]
            room = rooms.roombyid(cur.room_id)
            
            threads.append({'id':cur.id, 'summary':cur.summary, 'question':cur.question, 'date_started':cur.date_started, 'room':room})
        
    return threads
    

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
        # TODO instead of hardcoding the html elements in, make use of some kind of template so it can be reformatted easier
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
        
        
