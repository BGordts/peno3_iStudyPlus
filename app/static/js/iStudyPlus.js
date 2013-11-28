window.onload = function () {
	initialise();
}
var initialise = function () {
	var element = $(".is_sidepanel-student-list"),
		hoverClass = "is_sidepanel-list-hover",
		offsetClass = "is_sidepanel-list-offset";
		console.log(element);

	element.hover(function(){element.addClass(hoverClass)}, function(){element.removeClass(hoverClass)})
	.scroll(function(){scrollOffsetF(element, offsetClass)});

	$('#datepicker').datetimepicker({
                    pickTime: false
                });
                $('#starttimepicker').datetimepicker({
                    pickDate: false
                });
                $('#endtimepicker').datetimepicker({
                    pickDate: false
                });
};


var scrollOffsetF = function (element, offsetClass) {
	if (element.scrollTop() > 0) {
		if (!element.hasClass(offsetClass)) {
			element.addClass(offsetClass)
		}

	} else {
		if (element.hasClass(offsetClass)) {
			element.removeClass(offsetClass)
		}
	}
};