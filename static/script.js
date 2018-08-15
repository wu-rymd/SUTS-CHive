// access logged in user_id from other .js files
var loggedInID;

var app = angular.module('chiveApp', []);
app.controller('chiveCtrl', function($scope, $http, $location, $rootScope) {
    $scope.highSchools = [];
    $scope.loggedIn = false;
    $scope.signingUp = false;
    $scope.clubs = [];
    $scope.currentHighSchoolID = null;
    $scope.formmsg = "Welcome to C-Hive!";

    
    // store the logged in user_id on the clientside
    $scope.loggedID;
    loggedInID = $scope.loggedID;


    $scope.scrollTo = function(selectorString) {
	
	
	$('html,body').animate({
	    scrollTop: $(selectorString).offset().top
	}, 'slow');

	/*if (selectorString != ".high-school-search") {
	  $("#searchbar-high-school").val('');
	  $("#highSchoolResults").html('');

	  }
	  if (selectorString != ".club-search") {
	  //$("#searchbar-club").val('');
	  //$("#clubResults").html('');
	  //$("#clubResults").fadeOut(500);
	  } */
    }

    $scope.populateHighSchools = function() {
	console.log('TODO');
	$('.highSchoolResults').fadeOut(500);
	$scope.highSchools = [];
	$.getJSON('http://localhost:5000/schools', function(data) {
	    for (var i = 0; i < data.length; i++) {
		console.log(data[i]);
		$scope.highSchools.push({name: data[i].name, address: data[i].address, id: i});
	    }
	    $scope.$apply();
	})

	$('#highSchoolResults').css('display', 'none').fadeIn(500);

	// TODO move the high school code from the script.js.bak file here
	//$scope.highSchools.push({name: 'other school', address: '456 other street', id: 2});
    }

    $scope.populateClubs = function() {
	// TODO move the club code from the script.js.bak file here
	console.log('TODO');
	$('.clubResults').fadeOut(500);
	$scope.clubs = [];
	var searchVal = $("#searchbar-club").val();
	// show that we can get the high school id
	console.log($scope.currentHighSchoolID);
	$.getJSON('http://localhost:5000/club?school_id=1', function(data) {
	    for (var i = 0; i < data.length; i++) {
		console.log(data[i]);
		if (data[i].school_id === 1) {
		    $scope.clubs.push({name: data[i].name, description: data[i].description, id: i});
		}
	    }
	    $scope.$apply();

	} )
	//$scope.clubs.push({name: 'my lame club', description: 'this is a lame club', id: 2});

	$('#clubResults').css('display', 'none').fadeIn(500);
    }

    $scope.goToClub = function(clubId) {
	console.log('TODO');
    }

    $scope.highSchoolSelect = function(schoolId) {
	console.log(schoolId);
	console.log('TODO')
	 $scope.scrollTo('.club-search')
	 // TODO load all available clubs here instead
	 $scope.currentHighSchoolID = schoolId;
    }


    $scope.signUp = function() {
	$scope.signingUp = true;
    }
    
    $scope.login = function() {
	$scope.loggedIn = true;
    }
    
    //$scope.populateFeed = function(userID) {
    //$scope.feed = [];
    //$.getJSON('http://localhost:5000/')
    //}

    $scope.successLogin = function(username){


	$.getJSON('http://localhost:5000/user', function(data) {

	    for (var i = 0; i < data.length; i++) {

		if (data[i].username == username) {

		    // store the logged in user_id on the clientside
		    $scope.loggedID = data[i].id;
		    loggedInID = $scope.loggedID;


		    // POST all of logged in user's info -> /set
		    $.ajax({
			url: 'http://localhost:5000/setLogin',
			type: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({

			    id: data[i].id,
			    first_name: data[i].first_name,
			    last_name: data[i].last_name,
			    username: data[i].username,
			    school_id: data[i].school_id,
			    email: data[i].email,
			    created_on: data[i].created_on, 
	
			}),
			crossDomain: true,
		    });


		    
		    $scope.inExperience= true;
		    $scope.$apply();
		    return;
		}
	    }

	    $scope.formmsg = "Login invalid.";
	    $scope.$apply();

	}); // end json call
	
	$scope.inExperience = false;
    }





    $scope.register = function(firstName, lastName, username, email, password, password2, school, schoolAddress) {

	// are all fields filled in?
	if (firstName == undefined ||
	    firstName == "" ||
	    lastName == undefined ||
	    lastName == "" ||
	    username == undefined ||
	    username == "" ||
	    email == undefined ||
	    email == "" ||
	    password == undefined ||
	    password == "" ||
	    password2 == undefined ||
	    password2 == "" || 
	    school == undefined ||
	    school == "") {
	    
	    $scope.formmsg = "All fields required."
	    $scope.$apply();
	}

	
	else if (email.indexOf('@') == -1) {
	    $scope.formmsg = "Invalid e-mail."
	    $scope.$apply();
	}

	else if (password != password2) {
	    $scope.formmsg = "Passwords do not match."
	    $scope.$apply();
	}
	
	// form fields seem good from the surface...
	// check w/ database to see if valid registration...
	else {
	    
	    
	    $.getJSON('http://localhost:5000/user', function(data) {
		console.log("request returned");
		for (var i=0;i<data.length;i++){

		    
		    if (data[i].username == username) {
			console.log("username match found");
			$scope.formmsg = "That username already exists."
			$scope.$apply();
			return;
		    }

		    else if (data[i].email == email) {
			console.log("email match found");
			$scope.formmsg = "E-mail already registered."
			$scope.$apply();
			return;
		    }
		    
		} // end for loop


		

		$.ajax({
		    url: 'http://localhost:5000/user',
		    type: 'POST',
		    contentType: 'application/json',
		    data: JSON.stringify({
			first_name: firstName,
			last_name: lastName,
			username: username,
			email: email,
			schoolName: school,
			schoolAddress: schoolAddress,
		    }),
		    crossDomain: true,
		    success: function() {
			console.log("SUCCESS");
			$scope.formmsg = "Account successfully created!";
			$scope.$apply();
		    },
		    error: function() {
			console.log("ERROR");
			$scope.formmsg = "Error creating account.";
			$scope.$apply();
		    }
		});
				
		
		

	    }); // end getJSON call

	    
	} // end else

	
    } // end register
    


    setTimeout(function(){
	$scope.$apply();
    }, 50);

});
