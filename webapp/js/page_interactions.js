$("#option_list_cards_text").click(function () {
    $.get("htmlapi/get_all_cards", function (jsonRsp) {
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
  $.post("htmlapi/name_card",
      {uid: safeCardId,
        name: $(this).find("input")[0].value},
      function (result) {
        console.log(result);
      })
});

$("#option_clear_console").click(function () {
  request_console.empty();
});

$("#function-add-automation-form").submit(function (e) {
  e.preventDefault();
  switch ($('input[name=automation_type]:checked', '#function-add-automation-form').val()) {
    case "print":
      $.post("htmlapi/add_automation",
          {uid: safeCardId,
          name: $("#addautomation-setname-input").val(),
          type: "PRINT",
          script: $("#card-function-addautomation-printinput").val()},
          function(result) {
            // console.log(result);
            $("#addautomation-setname-input").val("");
            $("#card-function-addautomation-printinput").val("");
            addToTextConsole("Print automation: "+ result.name + " successfully added to " + currentCardName);
          });
      break;
    case "python":
      $.post("htmlapi/add_automation",
          {uid: safeCardId,
          name: $("#addautomation-setname-input").val(),
          type: "PYTHON",
          script: $("#card-function-addautomation-pythoninput").val()},
          function(result) {
            console.log(result);
            $("#addautomation-setname-input").val("");
            $("#card-function-addautomation-pythoninput").val("");
            addToTextConsole("Python automation: "+ result.name + " successfully added to " + currentCardName);
          });
      break;
    case "htmlRequest":
      $.ajax({
        data: {
          url: $("#card-function-add-automation-htmladdress").val(),
          data: null,
          type:$('input[name=htmlMethod]:checked', '#card-function-addautomation-html-div').val(),
          uid: safeCardId,
          name: $("#addautomation-setname-input").val()

        },
        url: "htmlapi/add_automation_html",
        type: "POST",
        success: function (res) {
          console.log(res);
          $("#card-function-add-automation-htmladdress").val("");
            $("#card-function-add-automation-htmlparams").val("");
            addToTextConsole("HTML automation: "+ res.name + " successfully added to " + currentCardName);
        },
        error: function (res) {
          console.log(res);
        }
      });
      break;
  }
});

$("#option_execute_automation").click(function () {
  let currentSafeId = safeCardId;
  let normalCardId = currentCardOnScanner;
  $.get("htmlapi/execute_automation", {uid: currentSafeId}, function (res) {
    addToTextConsole("Card Automation from " + normalCardId);
    addToTextConsole("Name: " + res.name);
    console.log(res);
    var htmlSafeSpan = $("<span></span>");
    //Create the span, append it to console, then add the text to it to prevent rendering html where unwanted.
    addToTextConsole(htmlSafeSpan);

    htmlSafeSpan.text("Output: " + res.result);
    console.log(res.result)
  });
});

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
  console.log("called");
  divs.forEach(function (elem) {
    if (elem !== dontHide) $(elem).toggleClass("gone", hideShow);
  })
}

setInterval(function () {
  $("#console_holder").scrollTop($("#console_holder")[0].scrollHeight);
}, 250);

findCardBtn.click(updateCardDetected);

//TODO: Finish sending net requests