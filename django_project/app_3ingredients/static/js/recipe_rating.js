$(document).ready(function() {
    $('.rating-form').submit(function (event) {
        event.preventDefault()
        const recipeId = $(this).attr('id')
        const ratingStatus = $(`#rate-${recipeId}`).text()
        const trimmedStatus = $.trim(ratingStatus)
        const url = $(this).attr('action')
        let ratingUpdated

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'recipe_id': recipeId,
                'value': trimmedStatus
            },
            success: function (response) {
                if(trimmedStatus === 'Looks delicious!') {
                    $(`#rate-${recipeId}`).text('Unlike')
                    ratingUpdated = response['rating']
                } else {
                    $(`#rate-${recipeId}`).text('Looks delicious!')
                    document.cookie = `rated_${recipeId}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
                    ratingUpdated = response['rating']
                }
                $(`#rating-${ recipeId }`).text(ratingUpdated)
            },
            error: function (response) {
                console.log('Request failed', response)
            }
        });
    });
});