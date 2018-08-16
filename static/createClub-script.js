// JavaScript file for create club page



var app = angular.module('createClubApp', []);
app.controller('createClubControl', function($scope) {

    $scope.message = "Register your club here!";

    $scope.createClub = function(clubName, description, category, location, usualTime) {

	// are all fields filled in?
	if ( clubName.$invalid ||
	     description.$invalid ||
	     category.$invalid ||
	     location.$invalid ||
	     usualTime.$invalid ) {
	   
	    $scope.message = "All fields required."
	}

	
	// form fields seem good from the surface...
	// check w/ database to see if valid registration...
	else {

	    var attendSchoolId;
	    var getOut = false;
	    $.getJSON('/getLogin', function(data) {

		attendSchoolId = data.loggedinSchoolId;

	    })
		.done( function(data) {

		    // check if already exists - look in attending school
		    $.getJSON('/club?school_id=' + attendSchoolId, function(data) {
			for (var i = 0; i < data.length; i++) {

			    // any matching club names at this school?
			    if (data[i].name == clubName){

				// remove following block after club pages complete

				getOut = true;
				$scope.message = "That club already exists!";
				$scope.$apply();

				// TODO redirect to existing club page
				
				return;
			    }
		 
			}  // end for loop

		    })
			.done( function(data) {

			    if (getOut)
				return;
			    
			    // create club
			    $.ajax({
				url: '/club',
				type: 'POST',
				contentType: 'application/json',
				data: JSON.stringify({
				    name : clubName,
				    school_id: attendSchoolId,
				    description: description,
				    category: category,
				    location: location,
				    usualTime: usualTime,
				}),
				crossDomain: true,
				success: function() {
				    $scope.message = "Club successfully created!";
				    $scope.$apply();
				},
			    });

			    
			})});

	    // --> TODO redirect to newly created club page
		
	} // end else

	
    } // end register
    
    

}); // end Angular app
