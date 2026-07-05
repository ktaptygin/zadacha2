$(document).ready(function () {
    $('a[href^="#"]').click(function (event) {
        var block = $(this).attr('href');

        if ($(block).length) {
            event.preventDefault();

            $('html, body').animate({
                scrollTop: $(block).offset().top
            }, 600);
        }
    });
});