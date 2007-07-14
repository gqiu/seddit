Seddit = Class.create();
Seddit.prototype = {
    initialize: function(options) {
        Object.extend(this, options);
        this.registerPoller();
    },
    
    downloadLog: function() {
        var threadId = this.threadId;
        new Ajax.Request('/api/poll/' + this.getThreadId.bind(this), {
            method: 'get',
            onSuccess: function(transport) {
                console.log(callback(this.threadId));
                var json = transport.responseText.evalJSON();
                var template = new Template("<tr class=\"message_row\" id=\"message_#{id}\"><td>#{user}</td><td>#{text}</td></tr>");
                                
                json.messages.message.each(function(message) {
                    new Insertion.Bottom('messages', template.evaluate(message));
           	    });
            }
        });
    },
    
    getThreadId: function() {
        return this.threadId;  
    },
    
    //  we're using this method, that just takes down the entire log every 3 seconds
    //  because i can't figure out javascripts scopes yet, and i need to get chatting
    //  working for the mid terms.
    //
    //      TODO: get checkPoll and downloadLog working.
    //              i could probably combine the two functions into one, if i really want
    //              to. they do essentiall the same thing.
    crappyUpdate: function() {
        var threadId = this.threadId;
        new Ajax.Request('/api/poll/' + threadId, {
            method: 'get',
            onSuccess: function(transport) {
                var json = transport.responseText.evalJSON();
                var template = new Template("<tr class=\"message_row\" id=\"message_#{id}\"><td>#{user}</td><td>#{text}</td></tr>");
                                
                var html = "";
                json.messages.message.each(function(message) {
                    html += template.evaluate(message);
           	    });
           	    
           	    $('messages').update(html);
            }
        }); 
    },
    
    checkPoll: function() {
        new Ajax.Request('/api/poll/' + 1, {
            method: 'get',
            onSuccess: function(transport) {
                var json = transport.responseText.evalJSON();
                new Insertion.Bottom('messages', '<p>hey</p>');
            }
        });
    },

    registerPoller: function() {
        this.crappyUpdate();
        new PeriodicalExecuter(this.crappyUpdate.bind(this), 3);
    }
};