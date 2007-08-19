import web
from app.utilities import auth2

class authtest:
    def GET(self):
        auth2.login('drew@revision1.net', 'pass')

        print auth2.authenticate()