
/* Auto open modal (for debugging) */
$(window).on('load', function(){
    /* $('#submit').modal('show');*/
});




$(document).ready(function() {
    /* Remember hiding panels */
    /* Close subscription box and save it as a cookie for 7 days */
    $("#close-subscription-box" ).click(function() {
	console.log("Subscription box closed!");
	Cookies.set('subscription_box_closed', 'yes', { expires: 7 });
    });	
    /* If a cookie isn't set - display the box (it's hidden by default). */
    if (Cookies.get('subscription_box_closed')==null) {
        $('.subscription-box').css("display","block");
    }


    /* Subscribed notification */
    var notification = $.query.get('notification');
    if (notification == "subscribed") {
	$(".alert").show();
	console.log("Subscription box closed!");
	Cookies.set('subscription_box_closed', 'yes', { expires: 7 });
	$(".alert").delay(3000).fadeOut();	
    }

    /* Search autocomplete */
    $('#searchbar').typeahead({
	source: [
            "Django",
            "React",
	]
    });
    $('#searchbar').typeahead()
    
    /* Search */
    $('#search-form').submit(function(event){
	/* Custom get request */
	event.preventDefault();
	event.stopPropagation();

	var query = $('#searchbar').val(); 
	var url = $.query.set('query', query);
	/* Send the get request */
	window.location = "/"+url;
    });

    /* Filtering */
    $('.dropdown-menu').on('click', 'a', function(e) {
	e.preventDefault();
	/* Grab the value */
	var value = $(this).attr('href');
	var filter = $(this).parent().parent().attr('id');
	/* Add the value to GET request */
	var url = $.query.set(filter, value);
	console.log(value);
	/* If the value is set back to default - remove it. */
	if (value == 'all' || value == 'hot') {
	    url = $.query.REMOVE(filter);	    
	}
	/* Go to the url */
	window.location = "/"+url;
    });





    
}); /* End document ready */

