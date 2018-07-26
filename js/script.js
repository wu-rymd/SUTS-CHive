function toScroll(selectorString) {
    // selectorString = selectorString.replace("link", "");

    $('html,body').animate({
        scrollTop: $(selectorString).offset().top
    }, 'slow');
}
