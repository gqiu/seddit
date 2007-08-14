import web
import config

from web import form

from app.models import people
from app.utilities import auth
from app.utilities import mail

view = web.template.render('app/views/people/', cache=config.cache)

loginform = form.Form(
    form.Textbox('email', form.notnull),
    form.Password('password', form.notnull),
    form.Hidden("error", value="False")
)

class dashboard:
    def GET(self):
        person = auth.getuser()
        print config.base.layout(view.dashboard(person), person)

class signup:
    # TODO add in error reporting
    def GET(self):
        print config.base.layout(view.signup())
        
    def POST(self):
        input = web.input()
        web.debug(input)

        # TODO alert user if the provided email is already in the system.
        if people.personexists(input.email):
            web.debug('email is already in the db')
            web.seeother('/signup/')
        
        # TODO alert user if passwords don't match
        if input.password == input.password_verify:
            password = auth.h(input.password)
            people.createperson(input.name, input.email, password)
            print 'hey! it worked!'
        else:
            web.debug('passwords dont match')
            web.seeother('/signup/')

class login:
    # TODO add a "forgot your password" feature
    def GET(self):
        f = loginform()
        print config.base.layout(view.login(f))
        
    def POST(self):
        f = loginform()
        
        if f.validates():
            password = auth.h(f.d.password)
            person = people.authenticate(f.d.email, password)
            
            if person:
                auth.setcookie(person)
                web.seeother('/dashboard/')
            else:
                print config.base.layout(view.login(f, error=True))
        else:
            print config.base.layout(view.login(f))
            
class logout:
    def GET(self):
        auth.logout()
        print 'logged out'
        
class list:
    def GET(self):
        people = people.getpeople()
        print config.base.layout(view.list(people))



# TODO change deleting, to deactivating.
class delete:
    def GET(self, id):
        web.debug(id)
        print 'hi'



class display: pass
class edit: pass
 