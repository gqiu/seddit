import web
import db
import config
import simplejson
import datetime

render = web.template.render('templates/', cache=config.cache)

def chat(**k):
    return render.chat()
    
def chat_as_json(**k):
    m_dataset = db.get_messages()    
    m_list = []
    
    for m in m_dataset:
        m_list.append({ 'id': m.id, 'user': m.author, 'text': m.message, 'time': '%s' % m.date_sent } )
        
    messages = { 'messages': { 'message': m_list } }
    print messages


web.template.Template.globals.update(dict(
  datestr = web.datestr,
  render = render
))