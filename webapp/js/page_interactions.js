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

$("input[name='automation_type']").change(function () {
  switch ($(this).val()) {
    case "print":
      $("#card-function-addautomation-printmsg-div").removeClass("gone");
      changeOtherAutomationInfoDivs(true, "#card-function-addautomation-printmsg-div");
      break;
    case "python":
      $("#card-function-addautomation-python-div").removeClass("gone");
      changeOtherAutomationInfoDivs(true, "#card-function-addautomation-python-div");
      break;
    case "htmlRequest":
      $("#card-function-addautomation-html-div").removeClass("gone");
      changeOtherAutomationInfoDivs(true, "#card-function-addautomation-html-div");
      break;
  }
});

function changeOtherAutomationInfoDivs(hideShow, dontHide) {
  if (dontHide.charAt(0) !== "#") dontHide = "#" + dontHide;
  const divs = ["#card-function-addautomation-html-div",
  "#card-function-addautomation-python-div",
  "#card-function-addautomation-printmsg-div"];

  divs.forEach(function (elem) {
    if (elem !== dontHide) $(elem).toggleClass("gone", hideShow);
  })
}

findCardBtn.click(updateCardDetected);

//TODO: Finish sending net requests