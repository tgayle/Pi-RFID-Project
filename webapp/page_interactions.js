
// deviceFoundBtn.click(function () {
//     waitingForCard.html("Device found!");
//     cardIDText.toggle(true);
//     cardOptionsDiv.toggle(600);
// });

// deviceRemovedBtn.click(function () {
//     waitingForCard.html("Waiting for card...");
//     cardIDText.toggle(false);
//     cardOptionsDiv.toggle(600);
// });

$("#option_list_cards_text").click(function () {
    $.get("php/get_all_cards.php", function (data) {
        const jsonRsp = JSON.parse(data);
        console.log(JSON.stringify(jsonRsp));

        jsonRsp.cards.forEach(function (card) {
            addToTextConsole(card.name + " (" + card.uid + ")");
        })
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

findCardBtn.click(updateCardDetected);
