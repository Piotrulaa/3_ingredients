$(function () {
    $('.scroll-top').on('shown.bs.collapse', function (event) {
            const recipeId = $(this).attr('id')
            $('html,body').animate({
                scrollTop: $(`#${recipeId}`).offset().top -50
            }, 250);
    });
});
