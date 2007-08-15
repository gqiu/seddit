import web
import config

from app.models import rooms
from app.models import threads
from app.utilities import auth

view = web.template.render('app/views/rooms/', cache=config.cache)

class listing:
    def GET(self):
        roomlist = rooms.getrooms()
        recentthreads = threads.recent()
        print config.base.layout(view.list(roomlist, recentthreads), auth.getuser())

class lobby:
    def GET(self, room):
        room = rooms.getroom(room)
        transcript = threads.threadtranscript(room.thread_id)
        person = auth.getuser()

        print config.base.thread(view.lobby(transcript.thread, transcript.messages, person))