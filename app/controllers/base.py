import web
import config

from app.utilities import auth

view = web.template.render('app/views/base/', cache=config.cache)

class index:
    def GET(self):
        web.seeother('/default/')
        
class default:
    def GET(self):
        person = auth.getuser()
        if person: web.seeother('/dashboard/')
        else:
            print config.base.layout(view.default(), person, title='home')