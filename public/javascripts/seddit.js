Seddit = Class.create();
Seddit.prototype = {
    initialize: function(options) {
        Object.extend(this, options);
        this.registerPoller();
        this.registerSender();
        
        Event.observe('set_author_name', 'click', this.setAuthor.bindAsEventListener(this));
    },
    
    setAuthor: function() {
        $F('message_author').getValue()  = $F('author_input');
        console.log($F('author_input'));
    },
    
    downloadLog: function() {
        var threadId = this.threadId;
        new Ajax.Request('/api/poll/' + this.getThreadId.bind(this), {
            method: 'get',
            onSuccess: function(transport) {
                console.log(callback(this.threadId));
                var json = transport.responseText.evalJSON();
                var template = new Template("<tr class=\"line\" id=\"message_#{id}\"><td class=\"author\">#{user}</td><td class=\"message\"><p>#{text}</p></td></tr>");
                                
                json.messages.message.each(function(message) {
                    new Insertion.Bottom('messages', template.evaluate(message));
           	    });
            }
        });
    },
    
    registerSender: function() {
        Event.observe('message_send', 'click', this.sendMessage.bindAsEventListener(this));
    },
    
    sendMessage: function() {
        console.log("clicked...");
        new Ajax.Request('/api/post', {
            method: 'post',
            parameters: $H({threadid: $F('thread_id'), author:$F('message_author'), message: $F('message_text')}),
            
            onSuccess: function(transport) {
                console.log('message sent');
                $F('message_content').reset();
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
                var template = new Template("<tr class=\"line\" id=\"message_#{id}\"><td class=\"author\">#{user}</td><td class=\"message\"><p>#{text}</p></td></tr>");
                                
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

Room = Class.create();
Room.prototype = {
    initialize: function(options) {
        Object.extend(this, options);
        this.registerListeners();
    },
    
    registerListeners: function() {
        Event.observe('create_room', 'click', this.createRoom.bind(this));
    },
    
    createRoom: function() {
        alert('creating...');
        new Ajax.Request('/api/room/new', {
           method: 'post',
           parameters: $H({title: $F('room_title'), url: $F('room_url'), description: $F('room_description')}),
           onSuccess: function(transport) {
               alert('created...');
           }
        });
    }
};
