window.onload = function() {
    screenFadeIn();
}


function goTo(linkString) {
    screenFadeOut();


    setTimeout( function() {
	window.location.href = linkString;
    }, 750);
}


function screenFadeIn() {
    $('body').css('display', 'none').fadeIn(1000);
}


function screenFadeOut() {
    $('body').fadeOut(500);
}


function toScroll(selectorString) {

    $('html,body').animate({
        scrollTop: $(selectorString).offset().top
    }, 'slow');


    setTimeout( function() {

	// cleanup

	if (selectorString != ".high-school-search") {
	    $("#searchbar-high-school").val('');
	    $("#highSchoolResults").html('');
	}

	else if (selectorString != ".club-search") {
	    $("#searchbar-club").val('');
	    $("#clubResults").html('');
	}



	if (selectorString == ".club-search")
	    populateClubs();
    }, 750);

}




function testHighSchool() {
    // test function
    $.getJSON('http://localhost:5000/schools', function(data) {
        var container = document.getElementById('highSchoolResults');
        html = "";
        for (var i=0;i<data.length;i++){
            console.log(data[i]);
            html += `
            <div class="card card-block card-outline-primary">

              <p class="card-text" id="0123"> <b>${data[i].name}</b> <br> ${data[i].address} &nbsp;
                    <span class="btn btn-outline-primary float-right" onclick="highSchoolSelect('${data[i].id}')">Select</span>
              </p>

            </div>
            `
        }
        container.innerHTML = html;
    });
}





function populateHighSchools() {


    $('.highSchoolResults').fadeOut(500);

    // get string input from input tag
    // dynamically creates & populates cards in container-results

    testHighSchool();


    $('#highSchoolResults').css('display', 'none').fadeIn(500);

}




function highSchoolSelect(highSchool) {
    // makes sure clubs to be searched in club-search view
    // is only from this high school

    toScroll('.club-search');
}






function testClub() {

    $.getJSON('http://localhost:5000/club?school_id=1', function(data){


	var container = document.getElementById('clubResults');
        html = "";
        for (var i=0;i<data.length;i++){
            console.log(data[i]);
            html += `
            <div class="card card-block card-outline-primary">

              <p class="card-text" id="0123"> <b>${data[i].name}</b> <br> ${data[i].description} &nbsp;
                    <span class="btn btn-outline-primary float-right" onclick="highSchoolSelect('0123')">Select</span>
              </p>

            </div>
            `
        }
        container.innerHTML = html;
    });
    
}






function populateClubs() {

    $('.clubResults').fadeOut(500);


    // get string input from input tag
    // dynamically creates & populates cards in container-results

    if ($("#searchbar-club").val() == "")
	showSuggestions();
    else
	searchClubs($("#searchbar-club").val());

    $('#clubResults').css('display', 'none').fadeIn(500);
}



function searchClubs(searchQuery) {
    // parses database for matches

    // test
    showAllClubs();
}




function showSuggestions() {


    var container = document.getElementById('clubResults');
    html = "";

    html += `
	<div class="container-suggestion">
	  <div class="btn btn-outline-primary" onclick="showAllClubs()" id="all-clubs">All clubs</div>
	  <div class="btn btn-outline-primary" onclick="showNewest()" id="newest-clubs">Newest clubs</div>
	  <div class="btn btn-outline-primary" onclick="showMostPopular()" id="most-popular">Most popular</div>
	</div>
`

    container.innerHTML = html;
}





function showAllClubs() {

    $('.clubResults').fadeOut(500);


    // populates all clubs, sorted by alphabetical order

    testClub();

    $('#clubResults').css('display', 'none').fadeIn(500);
}






function showNewest() {

    $('.clubResults').fadeOut(500);

    // show newest clubs on top by parsing database
    // for specified club creation date

    testClub();

    $('#clubResults').css('display', 'none').fadeIn(500);
}




function showMostPopular() {

    $('.clubResults').fadeOut(500);

    // show most popular clubs on top by parsing database
    // for specified club population size

    testClub();

    $('#clubResults').css('display', 'none').fadeIn(500);
}
