/*  Seddit.js
 *
 *  Copyright 2007 Drew Newberry <drew@revision1.net>
 *
/*-------------------------------------------*/
var Seddit = {}

Seddit.Transcript = Class.create();
Seddit.Transcript.prototype = {    
    initialize: function(options) {
        Object.extend(this, options);

        this.registerUpdaters();
        this.registerListeners();
    },

    registerListeners: function() {
        Event.observe('message_send', 'click', this.say.bindAsEventListener(this));
        Event.observe($('message_content'), 'keypress', this.keyPress.bindAsEventListener(this));
    },
    
    registerUpdaters: function() {
        new PeriodicalExecuter(this.poller.bind(this), 2);
    },
    
    keyPress: function(event) {
        switch(event.keyCode) {
            case Event.KEY_RETURN:
                if(event.shiftKey) {
                    return;
                } else {
                    this.say();
                }
                Event.stop(event);
        }
    },
    
    say: function() {
        console.log('saying something...');
        new Ajax.Request('/thread/' + this.id + '/say/', {
           method: 'post',
           parameters: $H({author: this.author_id, message:$F('message_content')}),
           onSuccess: function(transport) {
               console.log('message sent');
               Form.Element.clear('message_content');
           }.bind(this)
        });
    },
    
    poller: function(message) {
        new Ajax.Request('/thread/' + this.id + '/transcript/' + this.last_message + '/', {
             method: 'get',
             onSuccess: function(transport) {
                 var messages = transport.responseText.evalJSON();
                 var template = new Template("<tr class=\"line\" id=\"message_#{id}\"><td class=\"author\">#{author}</td><td class=\"message\"><p>#{content}</p></td></tr>");
                 var last = this.last_message;
                 
                 
                 var html = "";
                 messages.each(function(message) {
                      html += template.evaluate(message);
                      last = message.id;
                 });
                 
                 this.last_message = last;
                 
                 new Insertion.Bottom('messages', html);
                 Element.scrollTo('message_bottom');
                 // TODO use smart scrolling to bottom, right now if the user is looking back at the transcript, it will move him back to the bottom every two seconds.
             }.bind(this)
             // TODO research the bind function a bit more, i believe it's bad form to bind a function this way.
        });
    },
  
};

Seddit.Lobby = Class.create();
Seddit.Lobby.prototype = {
    initialize: function(options) {
        Object.extend(this, options);  
        
        this.registerListeners();
    },
    
    registerListeners: function() {
        Event.observe('new_question', 'click', this.newQuestion.bindAsEventListener(this));
    },
    
    newQuestion: function() {
        Modalbox.show($('new_question_modal', {title: 'Ask a new Question.', width: 300}));
    }
};

Seddit.Users = Class.create();
Seddit.Users.prototype = {
    initialize: function(options) {
        Object.extend(this, options);   
    }
};

