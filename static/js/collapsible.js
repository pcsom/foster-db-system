$(window).on('load', function() {
    var coll = $(`.collapsible`)
    coll.on("click", function() {
        $(this).toggleClass("active")
        var content = $(this).next()
        if (content.css("maxHeight") != "0px"){
            content.css("maxHeight", "0px")
            content.css("border-width", "0px")
        } else {
            content.css("maxHeight", content.prop("scrollHeight") + "px")
            content.css("border-width", "4px")
            setTimeout(function() {
                content.css("maxHeight", content.prop("scrollHeight") + "px")
            }, 200);
        }
    })
});