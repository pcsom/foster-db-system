var collFunc = function(elem) {
    elem.toggleClass("active")
    var content = elem.next()
    if (content.css("maxHeight") != "0px"){
        content.css("maxHeight", "0px")
        content.css("border-width", "0px")
    } else {
        content.css("maxHeight", content.prop("scrollHeight") + "px")
        content.css("border-width", "4px")

        //For special case where once expanded, content wraps around and flows down such that another maxheight assignment is needed
        setTimeout(function() {
            content.css("maxHeight", content.prop("scrollHeight") + "px")
        }, 100);
    }
}

function setCollSpecific (coll) {
    coll.on("click", function() {
        if ($(this).data('stopColl'))
        {
            console.log("block")
            $(this).data('stopColl', false)
            return
        }
        else {
            console.log("pass")
            collFunc($(this))
        }
    })
}

var collInit = function() {
    setCollSpecific($(`.collapsible`))
}


$(window).on('load', collInit);