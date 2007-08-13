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
    },
    
    registerUpdaters: function() {
        new PeriodicalExecuter(this.poller.bind(this), 4);
    },
    
    say: function() {
        console.log('saying something...');
        new Ajax.Request('/thread/' + this.id + '/say/', {
           method: 'post',
           parameters: $H({author: this.author_id, message:$F('message_content')}),
           onSuccess: function(transport) {
               console.log('message sent');
               $F('message_content').reset();
           }
        });
    },
    
    poller: function(message) {
        new Ajax.Request('/thread/' + this.id + '/transcript/' + this.last_message + '/', {
             method: 'get',
             onSuccess: function(transport) {
                 var messages = transport.responseText.evalJSON();
                 var template = new Template("<tr class=\"line\" id=\"message_#{id}\"><td class=\"author\">#{author_id}</td><td class=\"message\"><p>#{content}</p></td></tr>");

                 console.log(this.last_message);
                 
                 var html = "";
                 messages.each(function(message) {
                      html += template.evaluate(message);
                      this.last_message = message.id;
                 });
                 
                 new Insertion.Bottom('messages', html);
             }.bind(this)
             // TODO research the bind function a bit more, i believe it's bad form to bind a function this way.
        });
    },
  
};

Seddit.Lobby = Class.create();
Seddit.Transcript.prototype = {
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

