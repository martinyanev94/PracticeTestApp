console.log("1111", 1111);

// Main JS


// Accordion
$(".accordion-content").hide();
    
    $(".accordion-header").click(function() {
      if ($(this).hasClass("active")) {
        $(this).removeClass("active");
        $(this).next(".accordion-content").slideUp();
      } else {
        $(".accordion-header.active").removeClass("active");
        $(".accordion-content:visible").slideUp();

        $(this).addClass("active");
        $(this).next(".accordion-content").slideDown();
    }
});