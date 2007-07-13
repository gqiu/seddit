var Seddit = {};

Seddit.Chat = Class.create();
Seddit.Chat.prototype = {    
    initialize: function(options) {
        Object.extend(this, options);
        console.log(this.threadId);
        console.log(this.user);
        
        this.test = 1
        this.downloadLog();
        //this.registerPoller();
    },
    
    downloadLog: function() {
        new Ajax.Request('/api/poll/1', {
            method: 'get',
            onSuccess: function(transport) {
                var json = transport.responseText.evalJSON();
                var template = new Template("<tr class=\"message_row\" id=\"message_#{id}\"><td>#{user}</td><td>#{message}</td></tr>");
                
                console.log(json);
                
                json.messages.message.each(function(message) {
                    console.log(template.eval(message));
               	    new Insertion.Bottom('messages', template.eval(message));
           	    });
            } 
        });
    },
    
    checkPoll: function() {
        console.log(this.user);
        new Ajax.Request('/api/poll/' + 1, {
            method: 'get',
            onSuccess: function(transport) {
                var json = transport.responseText.evalJSON();
                new Insertion.Bottom('messages', '<p>hey</p>');
            }
        });
    },
    
    registerPoller: function() {
        new PeriodicalExecuter(this.checkPoll, 3);
    }
};