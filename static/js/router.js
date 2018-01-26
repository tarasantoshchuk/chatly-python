$(document).ready(function() {

function Account(data) {
  this.id = ko.observable(data.id);
  this.name = ko.observable(data.name);
  this.owner = ko.observable(data.owner);
}
function SharedAccount(data) {
  this.id = ko.observable(data.id);
  this.name = ko.observable(data.name);
}

function Transaction(data) {
  this.id = ko.observable(data.id);
  this.name = ko.observable(data.name);
  this.amount = ko.observable(data.amount);
  this.username = ko.observable(data.username)
}

function User(data) {
    this.username = ko.observable(data.username);
}

function AppViewModel() {
  var self = this;

  self.isAdmin = ko.observable(false);
  self.allAccounts = ko.observableArray([])
  self.accounts = ko.observableArray([]);
  self.sharedAccounts = ko.observableArray([]);
  self.transactions = ko.observableArray([]);
  self.accountUsers = ko.observableArray([]);
  self.accountOwner = ko.observable("");

  self.accountSummary = ko.observable(0);

  self.newAccountName = ko.observable("");
  self.newSharedAccountName = ko.observable("");

  self.newTransactionName = ko.observable("");
  self.newTransactionAmount = ko.observable(0);

  self.chosenHome = ko.observable(null);
  self.chosenAccountInfo = ko.observable(null);
  self.chosenAccountInfoData = ko.observable(null);
  self.chosenAddAccount = ko.observable(null);
  self.chosenAddTransaction = ko.observable(null);
  self.chosenAddSharedAccount = ko.observable(null);
  self.chosenEditAccount = ko.observable(null);

  self.addAccountSubmit = function(e) {
    $.post('/account', {
      name: self.newAccountName
    }).then(function(data) {
      self.newAccountName("");
      location.hash = "#/";
    }).catch(function(error) {

    })
  };

  self.editAccount = function(e) {
  $.ajax({
        url: '/account',
        type: 'PUT',
        data: {
            id: e.id,
            name: e.name
        },
        success: function() {
          location.hash = "#/account/" + e.id;
        },
        error: function(error) {

        }
    });
  }

  self.deleteAccount = function(e) {
    $.ajax({
        url: '/account',
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

  self.addSharedAccountSubmit = function(e) {
    $.post('/account_member', {
      id : self.chosenAccountInfoData().id,
      username: self.newSharedAccountName
    }).then(function(data) {
      self.newSharedAccountName("");
      location.hash = "#/account/" + self.chosenAccountInfoData().id
    }).catch(function(error) {
      console.log(error);
    })
  };
  self.addTransactionSubmit = function(e) {

    $.post('/add_transaction', {
      name: self.newTransactionName,
      amount: self.newTransactionAmount,
      account_id: self.chosenAccountInfoData().id
    }).then(function(data) {
      self.newTransactionName("");
      self.newTransactionAmount(0);
      location.reload();
    }).catch(function(error) {

    })
  };


  self.goToAddTransaction = function(acc) {
    location.hash = "#/transaction/" + acc.id
  }

  self.goToEditAccount = function(acc) {
    location.hash = "#/account/edit/" + acc.id
  }

  self.goToAccountDetails = function(acc) {
    location.hash = "#/account/" + acc.id();
  }

  Sammy("#main", function () {
    this.get('#/', function (context) {
      self.chosenAddAccount(null);
      self.chosenAccountInfo(null);
      self.chosenAccountInfoData(null);
      self.chosenAddTransaction(null);
      self.chosenAddSharedAccount(null);
      self.chosenEditAccount(null);

      $.get('/home').then(function(json) {
        self.isAdmin(JSON.parse(json).isAdmin);
        self.chosenHome("home");
        var mappedAllAccounts = $.map(JSON.parse(json).all_accounts, function(item) { return new Account(item) });
        self.allAccounts(mappedAllAccounts);
        var mappedAccounts = $.map(JSON.parse(json).accounts, function(item) { return new Account(item) });
        self.accounts(mappedAccounts);
        var mappedSharedAccounts = $.map(JSON.parse(json).shared_accounts, function(item) { return new SharedAccount(item) });
        self.sharedAccounts(mappedSharedAccounts);
        }).catch(function(error) {
          self.chosenHome(null);
          context.partial('../static/views/about.html').then(function() {});
      })
    });
    this.get('#/add_account', function (context) {
      self.chosenHome(null);
      self.chosenAccountInfo(null);
      self.chosenAddTransaction(null);
      self.chosenAddSharedAccount(null);
      self.chosenEditAccount(null);

      $.get('/home').then(function(json) {
        self.chosenAddAccount("add");
      })
    });
    this.get('#/add_shared_account', function (context) {
      self.chosenHome(null);
      self.chosenAccountInfo(null);
      self.chosenAddTransaction(null);
      self.chosenAddAccount(null);
      self.chosenEditAccount(null);
      self.chosenAddSharedAccount("add");
    });
    this.get('#/account/:id', function(context) {
      self.chosenHome(null);
      self.chosenAddAccount(null);
      self.chosenAddTransaction(null);
      self.chosenAddSharedAccount(null);
      self.chosenEditAccount(null);

      $.get('/account/' + context.params.id).then(function(json) {
        var account = JSON.parse(json).account;
        self.chosenAccountInfo(account);
        self.chosenAccountInfoData(account);
        var transactions = JSON.parse(json).transactions;

        var mappedTransactions = $.map(transactions, function(item) { return new Transaction(item) });
        self.transactions(mappedTransactions);
        var users = JSON.parse(json).users;
        var mappedUsers =  $.map(users, function(item) { return new User(item) });

        var owner = JSON.parse(json).owner;
        self.accountOwner(owner)
        self.accountUsers(mappedUsers)

        var amount = 0;
        transactions.forEach(function(t) {
          amount += t.amount;
        }, this);
        self.accountSummary(amount);


      })
    })
    this.get('#/account/edit/:id', function(context) {
        self.chosenHome(null);
        self.chosenAddAccount(null);
        self.chosenAddTransaction(null);
        self.chosenAddSharedAccount(null);
        self.chosenAccountInfo(null);
        self.chosenEditAccount({
            id: self.chosenAccountInfoData().id,
            name: self.chosenAccountInfoData().name
        });
    })
    this.get('#/transaction/:id', function(context) {
      self.chosenHome(null);
      self.chosenAddAccount(null);
      self.chosenAccountInfo(null);
      self.chosenAddSharedAccount(null);
      self.chosenEditAccount(null);
      self.chosenAddTransaction('transaction');
    })
  }).run("#/");
}

ko.applyBindings(new AppViewModel());
});
