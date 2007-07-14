import web
    
def room_list(**k):
    """ return a list of rooms.
    
        you can also drill down on the query by passing parameters on.
    """
    return web.select('rooms', **k)
    
def getlobbyid(name):
    """Return id of a room lobby, given a room name"""
    return getroom(name).thread_id

    
def getroom(name):
    """Return room from database given the url of the room"""
    return web.select('rooms', where='url = \'' + name + '\'', limit=1)[0]
    
def sendmessage(threadid, author, message):
    return web.insert('messages', thread_id=threadid, author=author, content=message)
    
def getlog(threadid):
    """Return an array of messages for a given thread id"""
    return web.select('messages', where='thread_id = \'' + threadid +'\'')
    
def getthreadupdates(threadid, lastid):
    """ Return an array of messages, offset by the last id given.
    
        by getting only new messages, it's a more efficient way for updating the thread.
    """
    return web.select('messages', where='thread_id = \'' + threadid +'\' AND id > ' + lastid)

    