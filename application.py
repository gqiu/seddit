import web
import view, config
import mimetypes
from view import render

from rooms import *
from api import *

urls = (
    '/(public)/.*',                 'public',
    
    '/',                            'index',
    '/default',                     'default',
    
    '/api/post',                    'api.post',
    '/api/poll/(\d+)',              'api.getlog',
    '/api/poll/(\d+)/offset/(\d+)', 'api.getthreadupdates',
    
    '/api/room/new',                'api.newroom',
    
    '/rooms',                       'rooms.overview',
    '/rooms/',                      'rooms.overview',
    '/rooms/(.*)',                  'rooms.room',
    '/rooms/(/.*)/threads',         'rooms.threadlist'
    '/rooms/(.*)/thread/(\d+)',     'rooms.thread'
)

class index:
    def GET(self):
        web.seeother('/default')

class default:
    def GET(self):
        print render.base(view.default())
        
class backend:
    def GET(self):
        view.chat_as_json()
        
    def POST(self):
        i = web.input()
        web.debug(i)
        web.insert('messages', seqname='message_id_seq', message = i.content, author = i.author)
        
        
def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream' 

class public:
    def GET(self, static_dir): 
        try:
            static_file_name = web.ctx.path.split('/')[-1]
            web.header('Content-type', mime_type(static_file_name))
            static_file = open('.' + web.ctx.path, 'rb').read()
            web.ctx.output = static_file
        except IOError:
            web.notfound()

if __name__ == "__main__":
    web.run(urls, globals(), *config.middleware)