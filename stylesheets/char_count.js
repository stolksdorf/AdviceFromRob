var box = $("charCount");
var trigger = $('[name|="adviceTweet"]');

$(document).ready(function () { 
	alert("test!");

	trigger.onkeyup = function(){ alert("hells yeah!"); };
}

