// JavaScript file for create club page
// Independent file



var app = angular.module('createClubApp', []);
app.controller('createClubControl', function($scope) {

    $scope.message = "Register your club here!";

    $scope.createClub = function(clubName, schoolName, schoolAddress, description) {

	// are all fields filled in?
	if (clubName == undefined ||
	    clubName == "" ||
	    schoolName == undefined ||
	    schoolName == "" ||
	    schoolAddress == undefined ||
	    schoolAddress == "" ||
	    description == undefined ||
	    description == "") {
	    
	    $scope.message = "All fields required."
	}

	
	// form fields seem good from the surface...
	// check w/ database to see if valid registration...
	else {

	    var matchSchoolId;
	    var getOut = false;
	    $.getJSON('http://localhost:5000/schools', function(data) {
		console.log("request returned");
		for (var i=0;i<data.length;i++){

		    if (data[i].name == schoolName && data[i].address == schoolAddress) {
			matchSchoolId = data[i].id;
			break;
		    }

		} // end for loop

	    })
		.done( function(data) {
		    
		    $.getJSON('http://localhost:5000/clubs', function(data) {
			for (var i = 0; i < data.length; i++) {

			    console.log(data[i].name);
			    console.log(clubName);
			    console.log(data[i].school_id);
			    console.log(matchSchoolId);
			    if (data[i].name == clubName && data[i].school_id == matchSchoolId){
				getOut = true;
				$scope.message = "That club already exists!";
				$scope.$apply();
				return;
			    }

		
			}  // end for loop

		    })
			.done( function(data) {

			    if (getOut)
				return;
			    
			    // create club
			    $.ajax({
				url: 'http://localhost:5000/club',
				type: 'POST',
				contentType: 'application/json',
				data: JSON.stringify({
				    name : clubName,
				    schoolName : schoolName,
				    schoolAddress : schoolAddress,
				    description : description,
				}),
				crossDomain: true,
				success: function() {
				    $scope.message = "Club successfully created!";
				    $scope.$apply();
				},
			    });

			    
			})});
		
	} // end else

	
    } // end register
    
    

}); // end Angular app
