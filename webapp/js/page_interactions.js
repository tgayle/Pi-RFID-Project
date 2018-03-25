$("#option_list_cards_text").click(function () {
    $.get("htmlapi/get_all_cards", function (jsonRsp) {
        // const jsonRsp = JSON.parse(data);
        console.log(JSON.stringify(jsonRsp));
        var dividerStr = "#########";
        addToTextConsole(dividerStr);
        jsonRsp.cards.forEach(function (card) {
            addToTextConsole(card.name + " (" + card.uid + ")");
        });
        addToTextConsole(dividerStr);
    });
});

$("#function-name-card-form").submit(function (e) {
  addToTextConsole("called");
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: "htmlapi/name_card",
    data:
        {uid: replaceAll(currentCardOnScanner, " ", ""),
        name: $(this).find("input")[0].value},
    success: function (re) {
      console.log(re)
      // alert("work");
    }
  });
  });

//
$("#cardFunctionsDiv").click(function() {
    $(this).removeClass("minimized-circle mx-auto my-auto");
});

$(".card-function-choice").click(function() {
    var thisInputBox = $(this).parent().find(".card-function");
    thisInputBox.toggleClass("hidden-card-function");
});

// Card Function Forms close btn
$("div i.command-cancel-form-btn").click(function() {
    $(this).closest(".card-function").addClass("hidden-card-function");
});

findCardBtn.click(updateCardDetected);
