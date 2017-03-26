// ===== Scroll to Top ====

$(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop() < 50) {
            $('#return-to-top').fadeOut(200);   // Else fade out the arrow
        } else {        // If page is scrolled more than 50px
            $('#return-to-top').fadeIn(200);    // Fade in the arrow
        }
    });
});
function top() {      // When arrow is clicked
    $('body,html').animate({
        scrollTop : 0                       // Scroll to top of body
    }, 500);
};