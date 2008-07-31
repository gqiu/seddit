import web

# connect to the database
web.config.db_parameters = dict(dbn='postgres', db='seddit_development', user='dnewberry', pw='')

web.webapi.internalerror = web.debugerror
middleware = [web.reloader]

# set template caching to false for debugging purposes
cache = False

# secret stuff for user auth see app.utilities.auth
# TODO should probably change to a better value
encryptionkey = 'something stored in some config file'

# mail settings for emailing passwords and whatnot
mailhost = 'localhost'
mailsender = 'admin@seddit'

# set our global base template
base = web.template.render('app/views/base/', cache=cache)

web.template.Template.globals.update(dict(
  datestr = web.datestr,
))
