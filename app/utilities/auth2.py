import web
import string, hmac
import time, datetime

#
#   refactored code is here...
#

SECRET = 'something stored in some config file'

def authenticate():
    """ return None if you aren't authenticated, or the person if you.
    
        it also returns None if the cookie is invalid.
        
        TODO implement "remember me"
    """
    cookie = web.cookies(_seddit=None)._seddit
    user = None
    
    if cookie:
        h, uid, t = cookie.split('/')
        
        
        user = web.select('people', where='id=%s' % web.sqlquote(uid))
        if user:
            user = user[0]
        else: # seddit has a guest user with an email of guest@seddit.local
            user = guest()
    else:
        web.setcookie('_seddit', '')
        user = guest()
        
    return user


def h(*l):
    return hmac.new(SECRET, repr(l)).hexdigest()
    
def login(email, password):
    password = h(password)
    user = getuser(email, password)
    
    if not user:
        return None
        print 'hi'
    else:
        print 'set cookie'
        text = cookie(user)
        web.setcookie('_seddit', text)
        print web.cookies()._seddit
        
        
def cookie(person):
    t = datetime.datetime(*time.gmtime()[:6]).isoformat()
    return '%s/%s/%s' % (h(person.id, person.email, t), person.id, str(t))
    
def logout():
    """ empties the seddit_session cookie, thus logging out the user
    """
    web.setcookie('seddit_session', '')
    
def getuser(email, password):
    """ return a user object if the email and passwords match an entry in the db.
    """
    user = web.select('people', where='email=%s and password=%s' % (web.sqlquote(email), web.sqlquote(password)), limit=1)
    if user:
        return user[0]
    else:
        return None
 
def generateguest():
    pass
    
def guest():
    """ returns our default guest user for those that aren't logged in
    
        when you want to chat, you still need to create a new guest user, but just for
        browsing we'll use thi temp user. this allows use to program user names and id
        into the templates without having to worry about there not being a user present.
    """
    return web.select('people', where='email=%s' % web.sqlquote('guest@seddit.local'))[0]