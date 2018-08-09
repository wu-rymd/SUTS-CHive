var app = angular.module('chiveApp', []);
app.controller('chiveCtrl', function($scope, $http, $location, $rootScope) {
    $scope.highSchools = [];
    $scope.loggedIn = false;
    $scope.clubs = [];
    $scope.currentHighSchoolID = null;
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
    $scope.login = function(username, password) {
	$scope.loggedIn = true;
	}
	
	$scope.populateFeed = function(userID) {
		$scope.feed = [];
		$.getJSON('http://localhost:5000/')
	}

});
