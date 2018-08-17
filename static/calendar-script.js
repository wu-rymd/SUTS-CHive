// JavaScript file for Shop Page

// References logged in user_id (/getLogin)


var app = angular.module('calendarApp', []);
app.controller('calendarControl', function($scope, $window) {

    $scope.showLogout = true;

    
    $.getJSON('/getLogin', function(data) {

	try {
	    if (data.loggedinID != undefined) {

    		$('#greetUser').html("<b> Hello, " + data.loggedinFirstName + "! </b>");

	    }

	    else {
    		$('#greetUser').html("You are not signed in. Contact an administrator for help. <br> &mdash; ClubHub Team");
		$('#greetUser').parent().nextAll().remove();
		return;
	    }
	}

	catch(err) {
    	    $('#greetUser').html("You are not signed in. Contact an administrator for help. <br> &mdash; ClubHub Team");
	    $('#greetUser').parent().nextAll().remove();

    	    console.log(err.message);
	    return;
	}

    });




    $scope.logout = function() {

	// POST all of logged in user's info -> /set
	$.ajax({
	    url: '/setLogin',
	    type: 'POST',
	    contentType: 'application/json',
	    data: JSON.stringify({

		message: 'Not logged in',

	    }),
	    crossDomain: true,

	    success: function() {
		$scope.loggedIn = false;
		$window.location.href = 'index.html';
	    },
	});

	$scope.showLogout = false;

    }


    $scope.goTo = function(link) {
	$window.location.href = link;
    }


}); // end Angular controller
