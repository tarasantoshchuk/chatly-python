$(function() {
    $('#home-btn').click(function() {
        $('#login-container').fadeOut(100);
        $('#main').delay(100).fadeIn(100);
    });
    $('#logout').click(function(e) {
        e.preventDefault();
        $.post('/logout', function() {
            location.reload()
        })
    })
    $('#login').click(function(e) {
        $('#main').fadeOut(100);
        $('#login-container').delay(100).fadeIn(100);
        e.preventDefault();
    });
    $('#login-form-link').click(function(e) {
    	$("#login-form").delay(100).fadeIn(100);
 		$("#register-form").fadeOut(100);
		$('#register-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	$('#register-form-link').click(function(e) {
		$("#register-form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$('#login-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
    $('#login-form').submit(function(e) {
        $.post('/login', {
            username: $('#login-form #username').val(),
            password: $('#login-form #password').val()
        }).then(function(data) {
            location.reload()
        }).catch(function(error) {

        })
        e.preventDefault();
    })
    $('#register-form').submit(function(e) {
        $.post('/register', {
            username: $('#register-form #username').val(),
            email: $('#register-form #email').val(),
            password: $('#register-form #password').val(),
            confirm_password: $('#register-form #confirm-password').val()
        }).then(function(data) {
            location.reload()
        }).catch(function(error) {

        })
        e.preventDefault();
    })
});
