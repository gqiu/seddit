import web

# connect to the database
web.config.db_parameters = dict(dbn='postgres', db='seddit_development', user='dnewberry', pw='')

web.webapi.internalerror = web.debugerror
middleware = [web.reloader]

# set template caching to false for debugging purposes
cache = False