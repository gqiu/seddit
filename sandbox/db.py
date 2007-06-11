import web
    
def get_messages(**k):
    return web.select('messages', **k)