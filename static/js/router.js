$(document).ready(function() {

function Chat(data) {
  this.id = ko.observable(data.id);
  this.name = ko.observable(data.name);
  this.owner = ko.observable(data.owner);
}
function SharedChat(data) {
  this.id = ko.observable(data.id);
  this.name = ko.observable(data.name);
}

function Message(data) {
  this.id = ko.observable(data.id);
  this.message = ko.observable(data.message);
  this.username = ko.observable(data.username)
}

function User(data) {
    this.username = ko.observable(data.username);
}

function AppViewModel() {
  var self = this;

  self.isAdmin = ko.observable(false);
  self.allChats = ko.observableArray([])
  self.chats = ko.observableArray([]);
  self.sharedChats = ko.observableArray([]);
  self.messages = ko.observableArray([]);
  self.chatUsers = ko.observableArray([]);
  self.chatOwner = ko.observable("");

  self.chatSummary = ko.observable(0);

  self.newChatName = ko.observable("");
  self.newSharedChatName = ko.observable("");

  self.newMessageName = ko.observable("");
  self.newMessageAmount = ko.observable(0);

  self.chosenHome = ko.observable(null);
  self.chosenChatInfo = ko.observable(null);
  self.chosenChatInfoData = ko.observable(null);
  self.chosenAddChat = ko.observable(null);
  self.chosenAddMessage = ko.observable(null);
  self.chosenAddSharedChat = ko.observable(null);
  self.chosenEditChat = ko.observable(null);

  self.addChatSubmit = function(e) {
    $.post('/chat', {
      name: self.newChatName
    }).then(function(data) {
      self.newChatName("");
      location.hash = "#/";
    }).catch(function(error) {

    })
  };

  self.editChat = function(e) {
  $.ajax({
        url: '/chat',
        type: 'PUT',
        data: {
            id: e.id,
            name: e.name
        },
        success: function() {
          location.hash = "#/chat/" + e.id;
        },
        error: function(error) {

        }
    });
  }

  self.deleteChat = function(e) {
    $.ajax({
        url: '/chat',
        type: 'DELETE',
        data: {
            id: e.id
        },
        success: function() {
          location.hash = "#/";
        },
        error: function(error) {

        }
    });
  }

  self.addSharedChatSubmit = function(e) {
    $.post('/chat_member', {
      id : self.chosenChatInfoData().id,
      username: self.newSharedChatName
    }).then(function(data) {
      self.newSharedChatName("");
      location.hash = "#/chat/" + self.chosenChatInfoData().id
    }).catch(function(error) {
      console.log(error);
    })
  };
  self.addMessageSubmit = function(e) {

    $.post('/add_message', {
      message: self.newMessageName,
      chat_id: self.chosenChatInfoData().id
    }).then(function(data) {
      self.newMessageName("");
      self.newMessageAmount(0);
      location.reload();
    }).catch(function(error) {

    })
  };


  self.goToAddMessage = function(acc) {
    location.hash = "#/message/" + acc.id
  }

  self.goToEditChat = function(acc) {
    location.hash = "#/chat/edit/" + acc.id
  }

  self.goToChatDetails = function(acc) {
    location.hash = "#/chat/" + acc.id();
  }

  Sammy("#main", function () {
    this.get('#/', function (context) {
      self.chosenAddChat(null);
      self.chosenChatInfo(null);
      self.chosenChatInfoData(null);
      self.chosenAddMessage(null);
      self.chosenAddSharedChat(null);
      self.chosenEditChat(null);

      $.get('/home').then(function(json) {
        self.isAdmin(JSON.parse(json).isAdmin);
        self.chosenHome("home");
        var mappedAllChats = $.map(JSON.parse(json).all_chats, function(item) { return new Chat(item) });
        self.allChats(mappedAllChats);
        var mappedChats = $.map(JSON.parse(json).chats, function(item) { return new Chat(item) });
        self.chats(mappedChats);
        var mappedSharedChats = $.map(JSON.parse(json).shared_chats, function(item) { return new SharedChat(item) });
        self.sharedChats(mappedSharedChats);
        }).catch(function(error) {
          self.chosenHome(null);
          context.partial('../static/views/about.html').then(function() {});
      })
    });
    this.get('#/add_chat', function (context) {
      self.chosenHome(null);
      self.chosenChatInfo(null);
      self.chosenAddMessage(null);
      self.chosenAddSharedChat(null);
      self.chosenEditChat(null);

      $.get('/home').then(function(json) {
        self.chosenAddChat("add");
      })
    });
    this.get('#/add_shared_chat', function (context) {
      self.chosenHome(null);
      self.chosenChatInfo(null);
      self.chosenAddMessage(null);
      self.chosenAddChat(null);
      self.chosenEditChat(null);
      self.chosenAddSharedChat("add");
    });
    this.get('#/chat/:id', function(context) {
      self.chosenHome(null);
      self.chosenAddChat(null);
      self.chosenAddMessage(null);
      self.chosenAddSharedChat(null);
      self.chosenEditChat(null);

      $.get('/chat/' + context.params.id).then(function(json) {
        var chat = JSON.parse(json).chat;
        self.chosenChatInfo(chat);
        self.chosenChatInfoData(chat);
        var messages = JSON.parse(json).messages;

        var mappedMessages = $.map(messages, function(item) { return new Message(item) });
        self.messages(mappedMessages);
        var users = JSON.parse(json).users;
        var mappedUsers =  $.map(users, function(item) { return new User(item) });

        var owner = JSON.parse(json).owner;
        self.chatOwner(owner)
        self.chatUsers(mappedUsers)

        var amount = 0;
        self.chatSummary(amount);


      })
    })
    this.get('#/chat/edit/:id', function(context) {
        self.chosenHome(null);
        self.chosenAddChat(null);
        self.chosenAddMessage(null);
        self.chosenAddSharedChat(null);
        self.chosenChatInfo(null);
        self.chosenEditChat({
            id: self.chosenChatInfoData().id,
            name: self.chosenChatInfoData().name
        });
    })
    this.get('#/message/:id', function(context) {
      self.chosenHome(null);
      self.chosenAddChat(null);
      self.chosenChatInfo(null);
      self.chosenAddSharedChat(null);
      self.chosenEditChat(null);
      self.chosenAddMessage('message');
    })
  }).run("#/");
}

ko.applyBindings(new AppViewModel());
});
