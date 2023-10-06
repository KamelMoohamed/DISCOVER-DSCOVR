$(document).ready(function () {
  $(".fa-bars").click(function () {
    $(this).toggleClass("fa-times");
    $(".nav").toggleClass("nav-toggle");
  });

  $(window).on("load scroll", function () {
    $(".fa-bars").removeClass("fa-times");
    $(".nav").removeClass("nav-toggle");

    if ($(window).scrollTop() > 10) {
      $("header").addClass("header-active");
    } else {
      $("header").removeClass("header-active");
    }
  });

  $(".facility").magnificPopup({
    delegate: "a",
    type: "image",
    gallery: {
      enabled: true,
    },
  });
});

// script.js
document.addEventListener("DOMContentLoaded", function () {
  var dateInput = document.getElementById("dateInput");

  dateInput.addEventListener("input", function () {
    var selectedDate = dateInput.value;
    console.log(selectedDate);
    $.ajax({
      type: "GET",
      url: `/predication/${selectedDate}`,
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function (data) {
        // Get and display the result
        plot(data);
      },
    });
  });
});

var currentDate = new Date();

// Format the current date as yyyy-mm-dd (required for the input type="date")
var formattedDate = currentDate.toISOString().substr(0, 10);

// Set the maximum date for the input element
document.getElementById("dateInput").setAttribute("max", formattedDate);
