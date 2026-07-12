$(document).ready(function () {
    var $sourceNav = $('.header__nav');
    var $sourceLogo = $('.header__logo-img');
    var fixedHeaderHtml = '<div class="header-fixed" aria-hidden="true"><div class="header-fixed__inner"></div></div>';

    $('body').append(fixedHeaderHtml);

    var $fixedHeader = $('.header-fixed');
    var $fixedInner = $('.header-fixed__inner');
    var $links = $sourceNav.find('.header__nav-link');
    var middleIndex = 4;

    $links.each(function (index) {
        if (index === middleIndex) {
            $fixedInner.append(
                '<a class="header-fixed__logo" href="#home">' +
                    '<img class="header-fixed__logo-img" src="' + $sourceLogo.attr('src') + '" alt="Hunger logo">' +
                '</a>'
            );
        }

        $fixedInner.append(
            '<a class="header-fixed__link" href="' + $(this).attr('href') + '">' + $(this).text().trim() + '</a>'
        );
    });

    function updateFixedHeader() {
        var shouldShow = $(window).width() >= 576 && $(window).scrollTop() > 100;

        $fixedHeader.toggleClass('is-visible', shouldShow);
        $fixedHeader.attr('aria-hidden', shouldShow ? 'false' : 'true');
    }

    function updateActiveLink() {
        var scrollPosition = $(window).scrollTop() + 100;
        var activeId = '#home';

        $('section[id], header[id]').each(function () {
            if ($(this).offset().top <= scrollPosition) {
                activeId = '#' + $(this).attr('id');
            }
        });

        $('.header-fixed__link').removeClass('is-active');
        $('.header-fixed__link[href="' + activeId + '"]').addClass('is-active');
    }

    updateFixedHeader();
    updateActiveLink();

    $(window).on('scroll resize', function () {
        updateFixedHeader();
        updateActiveLink();
    });

    $(document).on('click', 'a[href^="#"]', function (event) {
        var block = $(this).attr('href');

        if (block !== '#' && $(block).length) {
            event.preventDefault();

            var menuOffset = $(window).width() >= 576 ? 70 : 0;

            $('html, body').stop().animate({
                scrollTop: Math.max($(block).offset().top - menuOffset, 0)
            }, 600);
        }
    });

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
