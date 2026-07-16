$(document).ready(function () {
    var today = new Date().toISOString().split('T')[0];
    $('.booking__field[type="date"]').attr('min', today);

    var $sourceNav = $('.header__nav');
    var $sourceLogo = $('.header__logo-img');
    var fixedHeaderHtml = '<div class="header-fixed" aria-hidden="true"><div class="header-fixed__inner"></div></div>';

    $('body').append(fixedHeaderHtml);

    var $fixedHeader = $('.header-fixed');
    var $fixedInner = $('.header-fixed__inner');
    var $mobileHeader = $('.header-mobile');
    var $mobileMenu = $('.header-mobile__menu');
    var $mobileToggle = $('.header-mobile__toggle');
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

    function closeMobileMenu() {
        $mobileMenu.removeClass('is-open').attr('aria-hidden', 'true');
        $mobileToggle.removeClass('is-active').attr('aria-expanded', 'false');
        $('body').removeClass('mobile-menu-open');
    }

    function updateFixedHeader() {
        var windowWidth = $(window).width();
        var scrollTop = $(window).scrollTop();
        var showDesktopHeader = windowWidth >= 576 && scrollTop > 100;
        var showMobileHeader = windowWidth < 576 && scrollTop > 40;

        $fixedHeader.toggleClass('is-visible', showDesktopHeader);
        $fixedHeader.attr('aria-hidden', showDesktopHeader ? 'false' : 'true');
        $mobileHeader.toggleClass('is-visible', showMobileHeader);
        $mobileHeader.attr('aria-hidden', showMobileHeader ? 'false' : 'true');

        if (!showMobileHeader) {
            closeMobileMenu();
        }
    }

    function updateActiveLink() {
        var scrollPosition = $(window).scrollTop() + 100;
        var activeId = '#home';

        $('section[id], header[id]').each(function () {
            if ($(this).offset().top <= scrollPosition) {
                activeId = '#' + $(this).attr('id');
            }
        });

        $('.header-fixed__link, .header-mobile__link').removeClass('is-active');
        $('.header-fixed__link[href="' + activeId + '"], .header-mobile__link[href="' + activeId + '"]').addClass('is-active');
    }

    updateFixedHeader();
    updateActiveLink();

    $(window).on('scroll resize', function () {
        updateFixedHeader();
        updateActiveLink();
    });

    $mobileToggle.on('click', function () {
        var isOpen = $mobileMenu.hasClass('is-open');

        $mobileMenu.toggleClass('is-open', !isOpen);
        $mobileMenu.attr('aria-hidden', isOpen ? 'true' : 'false');
        $mobileToggle.toggleClass('is-active', !isOpen);
        $mobileToggle.attr('aria-expanded', isOpen ? 'false' : 'true');
        $('body').toggleClass('mobile-menu-open', !isOpen);
    });

    $('.header-mobile__link, .header-mobile__logo').on('click', closeMobileMenu);

    $(document).on('keydown', function (event) {
        if (event.key === 'Escape') {
            closeMobileMenu();
        }
    });

    $(document).on('click', 'a[href^="#"]', function (event) {
        var block = $(this).attr('href');

        if (block !== '#' && $(block).length) {
            event.preventDefault();

            var menuOffset = $(window).width() >= 576 ? 70 : 64;

            $('html, body').stop().animate({
                scrollTop: Math.max($(block).offset().top - menuOffset, 0)
            }, 600);
        }
    });

    if ($.fn.slick) {
        $('.specialties__slider').slick({
            arrows: false,
            dots: true,
            infinite: true,
            speed: 500,
            autoplay: true,
            autoplaySpeed: 5000,
            pauseOnHover: true
        });
    }

    $('.booking__form').on('submit', function (event) {
        event.preventDefault();

        var form = $(this);
        var button = form.find('.booking__button');
        var result = form.find('.booking__result');

        button.prop('disabled', true).text('SENDING...');
        result.addClass('d-none').removeClass('alert-success alert-danger').text('');

        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: form.serialize(),

            success: function (response) {
                result
                    .removeClass('d-none alert-danger')
                    .addClass('alert-success')
                    .text(response.message);

                form[0].reset();
            },

            error: function (xhr) {
                var message = 'Could not send the booking.';

                if (xhr.responseJSON && xhr.responseJSON.message) {
                    message = xhr.responseJSON.message;
                }

                result
                    .removeClass('d-none alert-success')
                    .addClass('alert-danger')
                    .text(message);
            },

            complete: function () {
                button.prop('disabled', false).text('BOOK NOW');
            }
        });
    });

    $('.contact__form').on('submit', function (event) {
        event.preventDefault();

        var form = $(this);
        var button = form.find('.contact__button');
        var result = form.find('.contact__result');

        button.prop('disabled', true).text('SENDING...');
        result.addClass('d-none').removeClass('alert-success alert-danger').text('');

        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: form.serialize(),

            success: function (response) {
                result
                    .removeClass('d-none alert-danger')
                    .addClass('alert-success')
                    .text(response.message);

                form[0].reset();
            },

            error: function (xhr) {
                var message = 'Could not send the message.';

                if (xhr.responseJSON && xhr.responseJSON.message) {
                    message = xhr.responseJSON.message;
                }

                result
                    .removeClass('d-none alert-success')
                    .addClass('alert-danger')
                    .text(message);
            },

            complete: function () {
                button.prop('disabled', false).text('SEND MESSAGE');
            }
        });
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