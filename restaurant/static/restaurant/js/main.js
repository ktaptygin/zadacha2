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

$(document).ready(function () {
    $('.menu__category').on('click', function () {
        var category = $(this).data('category');
        var isActive = $(this).hasClass('is-active');

        $('.menu__category').removeClass('is-active');

        if (isActive) {
            $('.menu__item').removeClass('is-hidden');
            return;
        }

        $(this).addClass('is-active');

        $('.menu__item').each(function () {
            if ($(this).data('category') === category) {
                $(this).removeClass('is-hidden');
            } else {
                $(this).addClass('is-hidden');
            }
        });
    });
});

