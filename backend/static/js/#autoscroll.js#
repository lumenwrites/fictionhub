function pageScroll(speed) {
    window.scrollBy(0,1);
    scroll = setTimeout(function(){pageScroll(speed);},speed);
}

Mousetrap.bind('s', function(e) {
    pageScroll(10);
});

Mousetrap.bind('shift+s', function(e) {
    window.clearTimeout(scroll);
});

Mousetrap.bind('esc', function(e) {
    // Set a fake timeout to get the highest timeout id
    var highestTimeoutId = setTimeout(";");
    for (var i = 0 ; i < highestTimeoutId ; i++) {
	clearTimeout(i); 
    }
});


Mousetrap.bind('d', function(e) {
    if (localStorage.getItem("darkInterface")) {
	localStorage.removeItem("darkInterface");
	$("link[href='/static/styles/dark.css']").remove();
	
    } else {
	localStorage.setItem("darkInterface", true);

	var headID = document.getElementsByTagName("head")[0];
	var cssNode = document.createElement('link');
	cssNode.type = 'text/css';
	cssNode.rel = 'stylesheet';
	cssNode.href = '/static/styles/dark.css';
	cssNode.media = 'screen';
	headID.appendChild(cssNode);
    }
});

$(document).ready(function() {
    if (localStorage.getItem("darkInterface")) {
	var headID = document.getElementsByTagName("head")[0];
	var cssNode = document.createElement('link');
	cssNode.type = 'text/css';
	cssNode.rel = 'stylesheet';
	cssNode.href = '/static/styles/dark.css';
	cssNode.media = 'screen';
	headID.appendChild(cssNode);
    }
});
