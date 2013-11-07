window.onload = function() {
    initialise()
}
var initialise = function() {
    var $sidepanel = $(".is_sidepanel-content")
    $sidepanel.hover(function() {$sidepanel.addClass("is_sidepanel-hover")},function() {$sidepanel.removeClass("is_sidepanel-hover")})
}


