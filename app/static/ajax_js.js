$(document).ready(function () {
  $(".add-button").on("click", function () {
    console.log($(this));
    console.log($(this).attr("id"));

    $.ajax({
      url: "/add",
      type: "POST",
      data: JSON.stringify({ response: $(this).attr("id") }),
      contentType: "application/json; charset=utf-8",
      dataType: "json",

      success: function (response) {
        element_id = "#game_" + response.response;
        $(element_id).text("Added to list");
        $(element_id).addClass("disabled");
      },
      error: function (error) {
        console.log(error);
      },
    });
  });
});

$(document).ready(function () {
  $(".remove-button").on("click", function () {
    console.log($(this));
    console.log($(this).attr("id"));

    $.ajax({
      url: "/remove",
      type: "POST",
      data: JSON.stringify({ response: $(this).attr("id") }),
      contentType: "application/json; charset=utf-8",
      dataType: "json",

      success: function (response) {
        element_id = "#my-game_" + response.response;
        $(element_id).fadeOut("normal", function() {
          $(this).remove();
        });
      },
      error: function (error) {
        console.log(error);
      },
    });
  });
});