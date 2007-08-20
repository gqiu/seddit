import web
import config

#   module: rooms

def getrooms():
    rooms = web.select('rooms')
    #  for room in rooms:
    #      room['threads'] = web.select('threads', where='room_id=%s' % web.sqlquote(room.id), limit=5)
    
    return rooms
    
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
        
def roombyid(id):
    room = web.select('rooms', where='id=%s' % web.sqlquote(id), limit=1)
    if room:
        return room[0]
    else:
        return None
        
def roomid(room):
    return getroom(room).id