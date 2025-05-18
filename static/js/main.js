//if (window.location.hostname != 'garzak.ir') {
//    alert('کپی رایت قالب را رعایت کرده و اقدام به خرید آن نمایید');
//    window.location.replace('http://rtlr.ir/258064');
//}

$(document).ready(function () {
    //Init the carousel
    $("#bid-s").owlCarousel({
        rtl: true,
        items: 1,
        autoplay: true,
        autoplayTimeout: 5000,
        loop: true,
        dots: false,
        onInitialized: startProgressBar,
        onTranslate: resetProgressBar,
        onTranslated: startProgressBar
    });
    
    function startProgressBar() {
      $(".slide-progress").css({
        width: "100%",
        transition: "width 5000ms"
      });
    }

    function resetProgressBar() {
      $(".slide-progress").css({
        width: 0,
        transition: "width 0s"
      });
    }
    // **************  product slider
    $(".product-carousel-catgory").owlCarousel({
        rtl: true,
        margin: 10,
        nav: true,
        navText: ['<i class="now-ui-icons arrows-1_minimal-right"></i>', '<i class="now-ui-icons arrows-1_minimal-left"></i>'],
        dots: false,
        responsiveClass: true,
        responsive: {
            0: {
                items: 2,
                slideBy: 1
            },
            576: {
                items: 2,
                slideBy: 1
            },
            768: {
                items: 4,
                slideBy: 2
            },
            992: {
                items: 4,
                slideBy: 2
            },
            1400: {
                items: 5,
                slideBy: 3
            }
        }
    });
    // **************  product slider
    $(".product-carousel").owlCarousel({
        rtl: true,
        margin: 10,
        nav: true,
        navText: ['<i class="now-ui-icons arrows-1_minimal-right"></i>', '<i class="now-ui-icons arrows-1_minimal-left"></i>'],
        dots: false,
        responsiveClass: true,
        responsive: {
            0: {
                items: 2,
                slideBy: 1
            },
            576: {
                items: 2,
                slideBy: 1
            },
            768: {
                items: 4,
                slideBy: 2
            },
            992: {
                items: 5,
                slideBy: 2
            },
            1400: {
                items: 6,
                slideBy: 3
            }
        }
    });

    // **************  product slider
    $(".Blog-carousel").owlCarousel({
        rtl: true,
        margin: 10,
        nav: true,
        navText: ['<i class="now-ui-icons arrows-1_minimal-right"></i>', '<i class="now-ui-icons arrows-1_minimal-left"></i>'],
        dots: false,
        responsiveClass: true,
        responsive: {
            0: {
                items: 2,
                slideBy: 1
            },
            576: {
                items: 2,
                slideBy: 1
            },
            768: {
                items: 3,
                slideBy: 2
            },
            992: {
                items: 4,
                slideBy: 2
            },
            1400: {
                items: 4,
                slideBy: 3
            }
        }
    });

    $('.brand-slider-cat .owl-carousel').owlCarousel({
        rtl: true,
        dots: false,
        loop: true,
        autoplay: true,
        autoplayHoverPause: true,
        smartSpeed: 200,
        responsive: {
            0: { items: 1 },
            1200: { items: 5 },
            992: { items: 5 },
            768: { items: 5 },
            600: { items: 3 },
            480: { items: 2 }
        }
    });

    $('.brand-slider-cat2 .owl-carousel').owlCarousel({
        rtl: true,
        dots: false,
        loop: true,
        autoplay: true,
        autoplayHoverPause: true,
        smartSpeed: 600,
        responsive: {
            0: { items: 1 },
            1200: { items: 4 },
            992: { items: 4 },
            768: { items: 5 },
            600: { items: 4 },
            480: { items: 2 }
        }
    });

    $('.brand-slider .owl-carousel').owlCarousel({
        rtl: true,
        dots: false,
        loop: true,
        autoplay: true,
        autoplayHoverPause: true,
        smartSpeed: 200,
        responsive: {
            0: { items: 1 },
            1200: { items: 7 },
            992: { items: 6 },
            768: { items: 5 },
            600: { items: 3 },
            480: { items: 2 }
        }
    });


    $('.back-to-top').click(function (e) {
        e.preventDefault();
        $('html, body').animate({ scrollTop: 0 }, 800, 'easeInExpo');
    });

    if ($("#img-product-zoom").length) {
        $("#img-product-zoom").ezPlus({
            zoomType: "inner",
            containLensZoom: true,
            gallery: 'gallery_01f',
            cursor: "crosshair",
            galleryActiveClass: "active",
            responsive: true,
            imageCrossfade: true,
            zoomWindowFadeIn: 500,
            zoomWindowFadeOut: 500
        });
    }

    $(".sum-more").click(function () {
        var sumaryBox = $(this).parents('.parent-expert');
        sumaryBox.find('.content-expert').toggleClass('active');
        sumaryBox.find('.shadow-box').fadeToggle();

        $(this).find('i').toggleClass('active');

        $(this).find('.show-more').fadeToggle(0);
        $(this).find('.show-less').fadeToggle(0);

    });

    $('nav.header-responsive li.active').addClass('open').children('ul').show();

    $("nav.header-responsive li.sub-menu> a").on('click', function () {
        $(this).removeAttr('href');
        var e = $(this).parent('li');
        if (e.hasClass('open')) {
            e.removeClass('open');
            e.find('li').removeClass('open');
            e.find('ul').slideUp(400);

        } else {
            e.addClass('open');
            e.children('ul').slideDown(400);
            e.siblings('li').children('ul').slideUp(400);
            e.siblings('li').removeClass('open');
        }
    });

    // Start scroll

    $(window).scroll(function () {
        if ($(this).scrollTop() > 60) {
            $("nav.header-responsive").css({ height: '60px' });
            $("nav.header-responsive .search-nav").css({ opacity: '0', visibility: 'hidden' });
        } else {
            $("nav.header-responsive").css({ height: '110px' });
            $("nav.header-responsive .search-nav").css({ opacity: '1', visibility: 'visible' });
        }
    });

    // End scroll
    
    // favorites product
    
    $("ul.gallery-options button.add-favorites").on("click",function () {
        $(this).toggleClass("favorites");
    });
    
    // favorites product

});







if (jQuery('.slider_main').length > 0) {
    jQuery(".slider_main").owlCarousel({
        rtl: true,
        dots: true,
        loop: true,
        autoplay: true,
        autoplayHoverPause: true,
        smartSpeed: 100,
        mouseDrag: true, 
        nav: true,
        navText: ["<div class='nav-btn prev-slide '><i class='fa fa-chevron-right'></i></div>", "<div class='nav-btn next-slide '><i class='fa fa-chevron-left'></i></div>"],
        responsive: {
            0: { items: 1, dots: false },
            1200: { items: 1},
            767: { items: 1},
            600: { items: 1, dots: false },
            480: { items: 1, dots: false }
        }
    });
}

jQuery(".recent-nav .next").on("click", function () {
    jQuery(".slider_main").trigger('next.owl.carousel');
});
jQuery(".recent-nav .prev").on("click", function () {
    jQuery(".slider_main").trigger('prev.owl.carousel');
});



document.addEventListener("DOMContentLoaded", function () {
  const rangeMin = document.getElementById("range-min");
  const rangeMax = document.getElementById("range-max");
  const minValue = document.getElementById("min-value");
  const maxValue = document.getElementById("max-value");
  const track = document.querySelector(".slider-track");

  const minGap = 1000;
  const max = 50000;

  function updateTrack() {
    const min = parseInt(rangeMin.value);
    const maxVal = parseInt(rangeMax.value);

    const percent1 = (min / max) * 100;
    const percent2 = (maxVal / max) * 100;

    track.style.background = `linear-gradient(to left, #e0e0e0 ${percent2}%, #61bec3 ${percent2}% ${percent1}%, #e0e0e0 ${percent1}%)`;

    minValue.textContent = min;
    maxValue.textContent = maxVal;
  }

  rangeMin.addEventListener("input", () => {
    if (parseInt(rangeMax.value) - parseInt(rangeMin.value) <= minGap) {
      rangeMin.value = parseInt(rangeMax.value) - minGap;
    }
    updateTrack();
  });

  rangeMax.addEventListener("input", () => {
    if (parseInt(rangeMax.value) - parseInt(rangeMin.value) <= minGap) {
      rangeMax.value = parseInt(rangeMin.value) + minGap;
    }
    updateTrack();
  });

  updateTrack();
});


 
/*slider speed*/
$('.carousel').carousel({
    interval: 50000
})



