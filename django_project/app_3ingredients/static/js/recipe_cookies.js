$(document).ready(function cookieStuff() {
    const recipes = document.getElementsByClassName("rating-form")
    var idArray = []
    for(var i = 0; i < recipes.length; i++) {
        var recipeId = $(recipes[i]).attr('id')
        idArray.push(recipeId)
    }
    for(var iter = 0; iter < idArray.length; iter++) {
        var recipe = idArray[iter];
        checkCookie(recipe);
    }
    return idArray

    function getCookie(cookieName) {
        var name = cookieName + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var cookieArray = decodedCookie.split(';');
        for(var i = 0; i < cookieArray.length; i++) {
            var cookie = cookieArray[i];
            while (cookie.charAt(0) == ' ') {
                cookie = cookie.substring(1);
            }
            if (cookie.indexOf(name) == 0) {
                return cookie.substring(name.length, cookie.length);
            }
        }
        return "";
    }

    function checkCookie(recipeId) {
        var cookie = getCookie(`rated_${recipeId}`);
        if (cookie != "") {
            $(`#rate-${recipeId}`).text('Unlike')
        } else {
            $(`#rate-${recipeId}`).text('Looks delicious!')
        }
    }
});