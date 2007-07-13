import web
import db
import config
import simplejson
import datetime

render = web.template.render('views/', cache=config.cache)

#
#   rooms
#
def roomsoverview():
    r = db.room_list()
    return render.rooms(r)
        
def roomlobby(name):
    id = db.getroomid(name)
    return render.lobby(id)
    
#
#   api
#



#
#   miscellaneous
#
def default(**k):
    return render.default()
    
def chat_as_json(**k):
    m_dataset = db.get_messages()    
    m_list = []
    
    for m in m_dataset:
        m_list.append({ 'id': m.id, 'user': m.author, 'text': m.message, 'time': '%s' % m.date_sent } )
        
    messages = { 'messages': { 'message': m_list } }
    
    web.header('Content-type', 'text/x-json')
    # web.header('X-Json', simplejson.dumps(messages))
    
    print simplejson.dumps(messages)


web.template.Template.globals.update(dict(
  datestr = web.datestr,
  render = render
))