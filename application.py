#! /usr/bin/env python

import web
import config
import app.controllers

urls = (
    '/(public)/.*',                         'app.controllers.public.public',
    '/about/',                              'app.controllers.base.about',
    '/help/',                               'app.controllers.base.help',
    
    '/test',                                'app.controllers.test.authtest',
                                            
    '/',                                    'app.controllers.base.index',
    '/default/',                            'app.controllers.base.default',
    '/dashboard/',                          'app.controllers.people.dashboard',
                                            
    '/rooms/',                              'app.controllers.rooms.listing',
    '/rooms/(.*)/lobby/',                   'app.controllers.rooms.lobby',
    '/rooms/threads/',                      'app.controllers.rooms.threadlist',
    '/rooms/thread/(\d+)',                  'app.controllers.rooms.thread',
     
    '/ask/',                                'app.controllers.threads.ask',                                       
    '/thread/new/',                         'app.controllers.threads.new',
    '/thread/(\d+)',                        'app.controllers.threads.chat',
    '/thread/(\d+)/transcript/',            'app.controllers.threads.transcript',
    '/thread/(\d+)/transcript/(\d+)/',      'app.controllers.threads.poll',        
    '/thread/(\d+)/say/',                   'app.controllers.threads.say',
    
    '/thread/(\d+)/resolve/',               'app.controllers.threads.resolve',
    '/thread/(\d+)/archive/',               'app.controllers.threads.archive',
    '/thread/(\d+)/archive/comment/',       'app.controllers.threads.comment',
                                            
    '/signup/',                             'app.controllers.people.signup',
    '/login/',                              'app.controllers.people.login',
    '/logout/',                             'app.controllers.people.logout',
    '/people/',                             'app.controllers.people.list',
    '/people/(\d+)/',                       'app.controllers.people.view',
    '/people/(\d+)/edit/',                  'app.controllers.people.edit',
    '/people/(\d+)/delete/',                'app.controllers.people.delete',
)

if __name__ == "__main__":
    web.run(urls, globals(), *config.middleware)