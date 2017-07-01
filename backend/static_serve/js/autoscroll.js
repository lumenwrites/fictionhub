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

function toggleFullScreen() {
    if ((document.fullScreenElement && document.fullScreenElement !== null) ||    
	(!document.mozFullScreen && !document.webkitIsFullScreen)) {
	if (document.documentElement.requestFullScreen) {  
	    document.documentElement.requestFullScreen();  
	} else if (document.documentElement.mozRequestFullScreen) {  
	    document.documentElement.mozRequestFullScreen();  
	} else if (document.documentElement.webkitRequestFullScreen) {  
	    document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);  
	}  
    } else {  
	if (document.cancelFullScreen) {  
	    document.cancelFullScreen();  
	} else if (document.mozCancelFullScreen) {  
	    document.mozCancelFullScreen();  
	} else if (document.webkitCancelFullScreen) {  
	    document.webkitCancelFullScreen();  
	}  
    }  
}
Mousetrap.bind('f', function(e) {
    var scrolled = $(document).scrollTop();
    toggleFullScreen();
    var doscroll = function(){$(document).scrollTop(scrolled);}
    setTimeout(doscroll,10);
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
