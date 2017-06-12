import Cookies from 'js-cookie';

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
    if (Cookies.get('subscription_box_closed')==null
	&& $.query.get('notification') != "subscribed") {
        $('.subscription-box').css("display","block");
    }

    /* Subscribed notification */
    var notification = $.query.get('notification');
    if (notification == "subscribed") {
	$(".alert").show();
	console.log("Subscription box closed!");
	Cookies.set('subscription_box_closed', 'yes', { expires: 500 });
	$(".alert").delay(3000).fadeOut();	
    }

    
    /* Search */
    $('#search-form').submit(function(event){
	/* Custom get request */
	event.preventDefault();
	event.stopPropagation();

	var query = $('#searchbar').val(); 
	var url = $.query.set('query', query);
	/* Send the get request */
	window.location = window.location.href + url;
    });

    /* Filtering */
    $('.query-filter').on('click', 'a', function(e) {
	e.preventDefault();
	/* Grab the value (Hot/Top or SciFi/Fantasy) */
	var value = $(this).attr('id');
	/* Grab the filter ("sorting" or "category")  */
	var filter = $(this).parent().parent().attr('id');
	/* Add the value to GET request */
	/* like ?sorting=top or ?category=SciFi */
	var url = $.query.set(filter, value);
	console.log(value);
	/* If the value is set back to default - remove it. */
	if (value == 'all' || value == 'hot') {
	    url = $.query.REMOVE(filter);	    
	}
	/* Go to the url */
	var current_url_without_query = window.location.href.split('?')[0];
	window.location = current_url_without_query+url;
    });

    /* Highlight search input if there's value in it*/
    if ($('#searchbar').val() && $('#searchbar').val().length > 0){
	$('#searchbar').addClass('active');
    }

    /* Google Analytics */
    /* 
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
	(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
			     m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
    ga('create', 'UA-44003603-19', 'auto');
    ga('send', 'pageview');
    */
    /* Tooltips */
    $('[data-toggle="tooltip"]').tooltip();


}); /* End document ready */

