import web
import config
from app.models import people

#   module: threads

def getmessages(id):
    return web.select('messages', where='thread_id=%s' % web.sqlquote(id), _test=False)
    
def new(roomid, summary, question):
    id = web.insert('threads', room_id=roomid, summary=summary, question=question)
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