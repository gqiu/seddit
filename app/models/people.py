import web
import config
from app.utilities import auth

#   module: people

def personexists(email):
    person = web.select('people', where='email=%s' % web.sqlquote(email))
    if not person:
        return False
    else:
        return True
        
def createperson(name, email, password):
    return web.insert('people', name=name, email=email, password=password)
    
def authenticate(email, password):
    person = web.select('people', where='email=%s AND password=%s' % (web.sqlquote(email), web.sqlquote(password)))
    if not person:
        return None
    else:
        return person[0]
        
def getpeople():
    return web.select('people')
    
def deactivate(id):
    # TODO implement deactivation.
    pass
    
def getperson(id):
    person = web.select('people', where = 'id=%s' % web.sqlquote(id), limit=1)
    
    if person:
        return person[0]
    else:
        return None