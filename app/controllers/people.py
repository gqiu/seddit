import web
import config

from web import form

from app.models import people
from app.models import threads
from app.utilities import auth
from app.utilities import mail


view = web.template.render('app/views/people/', cache=config.cache)

def getemail():
    input = web.input()
    try:
        if input.email:
            return input.email
        else:
            return ' '
    except AttributeError:
        pass

loginform = form.Form(
    form.Textbox('email', form.notnull),
    form.Password('password', form.notnull),
    form.Hidden("error", value="False")
)

signupform = form.Form(
    form.Textbox('name'),
    form.Textbox('email', value=getemail()),
    form.Password('password'),
    form.Password('password_verify'),
    validators = [form.Validator("Passwords don't match.", lambda i: i.password == i.password_verify)]
)

class dashboard:
    def GET(self):
        person = auth.getuser()
        recent = threads.getrecent(person.id)
        
        print config.base.layout(view.dashboard(person, recent), person)

class recent:
    def GET(self):
        person = auth.getuser()
        recent = threads.getrecent(person.id, limit=40)
        print config.base.layout(view.recent(recent), person)

class signup:
    # TODO add in error reporting
    def GET(self):
        f = signupform()
        print config.base.layout(view.signup(f))
        
    def POST(self):
        f = signupform()
        
        if f.validates():
            if(people.personexists(f.d.email)):
                print config.base.layout(view.signup(f, exists=True))
            else:
                password = auth.h(f.d.password)
                people.createperson(f.d.name, f.d.email, password)
                web.seeother('/login/')
        else:
            print config.base.layout(view.signup(f))
                
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
        web.seeother('/default/')
        
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
 