import web
import config

#   module: rooms

def getrooms():
    return web.select('rooms')
    
def getlobby(room):
    room = getroom(room)
    web.debug(room.title)
    return web.select('threads', where='', limit=1)
    
def getroom(room):
    room = web.select('rooms', where='url=%s' % web.sqlquote(room), limit=1)
    if room:
        return room[0]
    else:
        return None
        
def roomid(room):
    return getroom(room).id