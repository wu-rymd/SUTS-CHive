// JavaScript file for Account Page
// Dependencies: script.js
// References logged in user_id (/getLogin)


var app = angular.module('accountApp', []);
app.controller('accountControl', function($scope, $window) {
    $scope.loggedID;
    $scope.loggedSchoolId;
    $scope.showLogout = true;
    $scope.clubs = [];

    $.getJSON('http://localhost:5000/getLogin', function(data) {

	
	try {
	    if (data.loggedinID != undefined) {

		$.getJSON('http://localhost:5000/schools', function(schoolData) {
		    for (var i = 0; i < schoolData.length; i++) {
			if (schoolData[i].id == data.loggedinSchoolId) {
			    $scope.loggedSchoolId = schoolData[i].id;
			    $('#schoolName').html("You attend <b>" + schoolData[i].name + "</b>");
			    break;
			}
		    }
		});
		
    		$('#greetUser').html("<b> Hello, " + data.loggedinFirstName + "! </b>");

		$('#fullName').html("Your name is <b>" + data.loggedinFirstName + " " + data.loggedinLastName + "</b>");
		$('#username').html("Your username is <b>" + data.loggedinUsername + "</b>");
		$('#email').html("Your e-mail is <pre>" + data.loggedinEmail + "</pre>");
		$('#createdOn').html("Your account was created on <pre>" + data.loggedinCreatedOn + "</pre>");

		$scope.loggedID = data.loggedinID;
		$scope.showLogout = true;


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
	
    })
	.done( function(data) {



	    

	    var clubNames = [];
	    var clubIDs = [];
	    
	    // access UserToClub mapping table
	    // push clubs that match user_id (var $scope.loggedID)

	    $.getJSON('http://localhost:5000/subscriptions', function(data) {

		for (var i = 0; i < data.length; i++) {

		    
		    if ( data[i].user_id == $scope.loggedID ) 
			clubIDs.push(data[i].club_id);
		}

		console.log('a');
	    })
		.done( function(data) {


		    
		    if (clubIDs.length == 0) {
			$('.clubList').html("<b> Uh oh! </b>You don't seem to be following any clubs! <span class='btn btn-outline-success float-right' ng-click=''>Discover</span>");
		    }

		    
		    $.getJSON('http://localhost:5000/club?school_id=' + $scope.loggedSchoolId, function(data) {

			for (var i = 0; i < clubIDs.length; i++) {
			    for (var j = 0; j < data.length; j++) {
				if ( data[j].id == clubIDs[i] ) {
				    clubNames.push(data[j].name);
				    $scope.clubs.push({name: data[j].name, id: clubIDs[i]});
				    $scope.$apply();
				}
			    }
			} // O(n^2) ... to be optimized later ... solves concern w/ async for now
		    });



		    console.log('b');
		})

	});
    

    $scope.unsubscribe = function(userId, clubId) {

	
	// remove link btwn userID and clubID in UserClubPosition mapping table
	$.ajax({
	    url: 'http://localhost:5000/unsubscribe',
	    type: 'DELETE',
	    contentType: 'application/json',
	    data: JSON.stringify({
		user_id: userId,
		club_id: clubId,
	    }),
	    crossDomain: true,
	    success: function() { console.log("SUCCESS"); },
	});


	// immediately removes club card from container
	for (var i = 0; i < $scope.clubs.length; i++) {
	    if ($scope.clubs[i].id == clubId)
		$scope.clubs.splice(i, 1);
	}


	if ($scope.clubs.length == 0) {
	    $('.clubList').html("<b> Uh oh! </b>You don't seem to be following any clubs! <span class='btn btn-outline-success float-right' ng-click=''>Discover</span>");
	}
	
    }


    $scope.logout = function() {
	
	// POST all of logged in user's info -> /set
	$.ajax({
	    url: 'http://localhost:5000/setLogin',
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
    
}); // end Angular controller


