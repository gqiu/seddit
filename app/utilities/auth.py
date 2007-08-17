import string
import hmac
import web
import config
import time, datetime
import app.models.people # must use fully qualified name to prevent errors.

# thanks infogami!
SECRET = config.encryptionkey

def genpassword():
    import random
    n = random.randint(8, 16)
    chars = string.letters + string.digits
    password = "".join([random.choice(chars) for i in range(n)])
    return password

def setcookie(user, remember=False):
    text = cookie(user)
    expires = (remember and 3600*24*7) or ''
    web.setcookie("seddit_session", text, expires=expires)
    
def logout():
    web.setcookie('seddit_session', '')
    
def h(*l):
    return hmac.new(SECRET, repr(l)).hexdigest()
    
def cookie(user):
    t = datetime.datetime(*time.gmtime()[:6]).isoformat()
    return '%s/%s/%s' % (h(user.id, user.password, t), user.id, str(t))
    
def validatecookie(cookie, user):
    hash, uid, t = cookie.split('/')
    return user.id == uid and hash == h(user.id, user.password, t) and t > time.time() - 60*60*24*365
    
def getuser():
    # TODO anyone can be any user by just having the id, fix it so it actually authenticates you.
    session = web.cookies().seddit_session
    
    if session:
        digest, userid, time = session.split('/')
        return app.models.people.getperson(userid)
        