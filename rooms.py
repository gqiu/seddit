import view
from view import render

class overview:
    def GET(self):
        print render.base(view.roomsoverview())
        
class room:
    def GET(self, name):
        print render.base(view.roomlobby(name))
        
class thread:
    def GET(self, room, threadid):
        pass
        
class threadlist:
    def GET(self, room):
        pass