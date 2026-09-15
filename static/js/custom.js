(function($) {
    'use strict'; // Start of use strict

    $(window).on("load scroll", function() {

        /*------------------------------------------------------------------
        Loader
        ------------------------------------------------------------------*/
        $("#dvLoading").fadeOut("fast");

        /*------------------------------------------------------------------
        Animation Numbers
        ------------------------------------------------------------------*/
        $('.animateNumber').each(function() {
            var num = $(this).attr('data-num');

            var top = $(document).scrollTop() + ($(window).height());
            var pos_top = $(this).offset().top;
            if (top > pos_top && !$(this).hasClass('active')) {
                $(this).addClass('active').animateNumber({
                    number: num
                }, 2000);
            }
        });
        $('.animateProcent').each(function() {
            var num = $(this).attr('data-num');
            var percent_number_step = jQuery.animateNumber.numberStepFactories.append('%');
            var top = $(document).scrollTop() + ($(window).height());
            var pos_top = $(this).offset().top;
            if (top > pos_top && !$(this).hasClass('active')) {
                $(this).addClass('active').animateNumber({
                    number: num,
                    numberStep: percent_number_step
                }, 2000);
                $(this).css('width', num + '%');
            }
        });
    });
    /*---------------------------------------------------------------------
    Magnific Popup Demo link : http://dimsemenov.com/plugins/magnific-popup
    ------------------------------------------------------------------------*/
    if ($('.front-gallery, .gallery-section').length) {

        $('.front-gallery, .gallery-section').magnificPopup({
            delegate: 'a',
            type: 'image',
            tLoading: 'Loading image #%curr%...',
            mainClass: 'mfp-img-mobile',
            gallery: {
                enabled: true,
                navigateByImgClick: true,
                preload: [0, 1]
            },
            image: {
                tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
                titleSrc: function(item) {
                    return item.el.attr('title') + '<small>by sbtechnosoft</small>';
                }
            }
        });
    }
    if ($('.image-popup-no-margins').length) {

        $('.image-popup-no-margins').magnificPopup({
            type: 'image',
            closeOnContentClick: true,
            closeBtnInside: false,
            fixedContentPos: true,
            mainClass: 'mfp-no-margins mfp-with-zoom',
            image: {
                verticalFit: true
            },
            zoom: {
                enabled: true,
                duration: 300
            }
        });
    }
    /*---------------------------------------------------------------------
    Gallery Post Hove Effect for Caption Script
    ------------------------------------------------------------------------*/
    function gallery_hover() {

        if ($(".gallery-caption img").length) {
            $(".gallery-caption img").on('mouseover', function() {
                var img_width = $(".gallery-caption img").width();
                var img_height = $(".gallery-caption img").height();
                $(".gallery-caption .blur").css({
                    "height": img_height,
                    "width": img_width
                });
            });
        }
    }
    gallery_hover();
    /*---------------------------------------------------------------------
    Image Filter Script 
    ------------------------------------------------------------------------*/
    var $container = $('.portfolioContainer');

    if ($('.portfolioFilter').length) {

        $('.portfolioFilter a').on('click', function() {

            $('.portfolioFilter .current').removeClass('current');
            $(this).addClass('current');
            var selector = $(this).attr('data-filter');
            $container.isotope({
                filter: selector,
                animationOptions: {
                    duration: 750,
                    easing: 'linear',
                    queue: false
                }
            });
            return false;
        });
    }
    /*------------------------------------------------------------------
    Count Down
    ------------------------------------------------------------------*/
    $('#jcountdown').countdown('2018/06/13 00:00:00', function(event) {
        var $this = $(this).html(event.strftime('' +
            '<span class="countdown-row countdown-show4"><span class="countdown-section"><span class="countdown-amount">%-D</span> <span class="countdown-period">days</span></span>' +
            '<span class="countdown-section"><span class="countdown-amount">%H</span> <span class="countdown-period">Hours</span></span>' +
            '<span class="countdown-section"><span class="countdown-amount">%M</span> <span class="countdown-period">Minutes</span></span>' +
            '<span class="countdown-section"><span class="countdown-amount">%S</span> <span class="countdown-period">Seconds</span></span></span>'));
    });
    //MobileMenu Activated
    $('.mainmenu-area').find('nav').meanmenu();

    /*------------------------------------------------------------------
     Scroll Top
     ------------------------------------------------------------------*/
    $.scrollUp({
        scrollText: '<i class="fa fa-angle-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    });
    /*------------------------------------------------------------------
    	theme color change
    ------------------------------------------------------------------*/
    var theme_settings = $(".theme-settings").find(".theme-color");
    theme_settings.on('click', function() {
        var val = $(this).attr('data-color');
        $('#style_theme').attr('href', 'css/' + val + '.css');
        $(".logo-change").attr('src', 'images/logo-' + val + '.png');
        $(".footer-logo-change").attr('src', 'images/footer-logo-' + val + '.png');
        theme_settings.removeClass('theme-active');
        theme_settings.addClass('theme-active');
        return false;
    });
    $(".theme-click").on('click', function() {
        $("#switcher").toggleClass("active");
        return false;
    });

})(jQuery);