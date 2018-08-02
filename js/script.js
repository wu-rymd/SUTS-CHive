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

    if (selectorString != ".high-school-search") {
      $("#searchbar-high-school").val('');
      $("#highSchoolResults").html('');
    }
    else if (selectorString != ".club-search") {
      $("#searchbar-club").val('');
      $("#clubResults").html('');
    }
  }

  $scope.populateHighSchools = function() {
    console.log('TODO');
    // TODO move the high school code from the script.js.bak file here
    $scope.highSchools.push({name: 'my school', address: '123 some street', id: 1});
    $scope.highSchools.push({name: 'other school', address: '456 other street', id: 2});
  }

  $scope.populateClubs = function() {
    // TODO move the club code from the script.js.bak file here
    console.log('TODO');
    $('.clubResults').fadeOut(500);
    var searchVal = $("#searchbar-club").val();
    // show that we can get the high school id
    console.log($scope.currentHighSchoolID);
    $scope.clubs.push({name: 'my cool club', description: 'this is a club', id: 1});
    $scope.clubs.push({name: 'my lame club', description: 'this is a lame club', id: 2});

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
});
